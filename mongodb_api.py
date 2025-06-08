
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from bson import ObjectId
from llm_service import call_gemini
from dotenv import load_dotenv
import os
import logging

# === Logging Config ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === Flask App Init ===
app = Flask(__name__)
load_dotenv()

# === Load Environment Variables ===
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not MONGO_URI:
    logging.critical("MONGO_URI not found in environment variables")
    exit(1)

if not DATABASE_NAME:
    logging.critical("DATABASE_NAME not found in environment variables")
    exit(1)

if not COLLECTION_NAME:
    logging.critical("COLLECTION_NAME not found in environment variables")
    exit(1)

logging.info(f"Connecting to MongoDB at: {MONGO_URI}")

# === MongoDB Setup ===
try:
    client = MongoClient(
        MONGO_URI,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    client.admin.command("ping")
    logging.info("MongoDB connection successful.")

    db = client[DATABASE_NAME]
    mycol = db[COLLECTION_NAME]

    try:
        sample = mycol.find_one()
        if sample:
            logging.info(f"Sample document from collection: {sample.get('_id', 'unknown')}")
        else:
            logging.warning("No documents found in collection.")
    except Exception as e:
        logging.warning(f"Error fetching sample document: {e}")

except (ServerSelectionTimeoutError, ConfigurationError, Exception) as e:
    logging.critical(f"MongoDB connection failed: {e}")
    exit(1)

# === Helper Functions ===

def get_article_by_id(article_id):
    try:
        logging.info(f"Looking up article ID: {article_id}")
        article = mycol.find_one({"_id": ObjectId(article_id)})
        if article:
            logging.info("Article found.")
        else:
            logging.warning("Article not found.")
        return article
    except Exception as e:
        logging.error(f"Error in get_article_by_id: {e}")
        return None

def convert_objectid_to_string(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid_to_string(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid_to_string(i) for i in obj]
    return obj

# === Routes ===

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Article Details and Summary API",
        "version": "1.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /article-details": "Get full article details by ID",
            "POST /article-summary": "Get article details with AI summary",
            "POST /summarize": "Get title and summary only"
        }
    })

@app.route("/health", methods=["GET"])
def health_check():
    try:
        client.admin.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"
    return jsonify({
        "status": "healthy",
        "database": db_status
    })

@app.route("/article-details", methods=["POST"])
def get_article_details():
    try:
        data = request.get_json(force=True)
        article_id = data.get("article_id")
        if not article_id:
            logging.warning("No article_id provided.")
            return jsonify({"error": "article_id is required"}), 400

        article = get_article_by_id(article_id)
        if not article:
            return jsonify({"error": f"Article with ID {article_id} not found"}), 404

        article_json = convert_objectid_to_string(article)
        return jsonify({"success": True, "article": article_json})

    except Exception as e:
        logging.exception("Error in get_article_details")
        return jsonify({"error": f"Internal server error: {e}"}), 500

@app.route("/article-summary", methods=["POST"])
def get_article_with_summary():
    try:
        data = request.get_json(force=True)
        article_id = data.get("article_id")
        if not article_id:
            logging.warning("No article_id provided.")
            return jsonify({"error": "article_id is required"}), 400

        article = get_article_by_id(article_id)
        if not article:
            return jsonify({"error": f"Article with ID {article_id} not found"}), 404

        title = article.get("title", "")
        meta_desc = article.get("meta", {}).get("description", "")
        combined_text = f"{title} {meta_desc}".strip()

        logging.info(f"Generating summary for article: {article_id}")
        summary = call_gemini("summary", context_vars={"text": combined_text}) if combined_text else "No content to summarize."

        response = {
            "success": True,
            "article": convert_objectid_to_string(article),
            "extracted_data": {
                "title": title,
                "meta_description": meta_desc,
                "combined_text": combined_text
            },
            "ai_summary": summary
        }
        return jsonify(response)

    except Exception as e:
        logging.exception("Error in get_article_with_summary")
        return jsonify({"error": f"Internal server error: {e}"}), 500

@app.route("/summarize", methods=["POST"])
def summarize_article():
    try:
        data = request.get_json(force=True)
        article_id = data.get("article_id")
        if not article_id:
            logging.warning("No article_id provided.")
            return jsonify({"error": "article_id is required"}), 400

        article = get_article_by_id(article_id)
        if not article:
            return jsonify({"error": f"Article with ID {article_id} not found"}), 404

        title = article.get("title", "")
        meta_desc = article.get("meta", {}).get("description", "")
        summary_meta = call_gemini("summary", context_vars={"text": f"{title} {meta_desc}"}) if (title or meta_desc) else "No data to summarize."

        return jsonify({"title": title, "summary": summary_meta})

    except Exception as e:
        logging.exception("Error in summarize_article")
        return jsonify({"error": f"Internal server error: {e}"}), 500

# === Start Server ===
if __name__ == "__main__":
    logging.info("Starting Flask app on port 8002...")
    app.run(host="0.0.0.0", port=8002, debug=True)
