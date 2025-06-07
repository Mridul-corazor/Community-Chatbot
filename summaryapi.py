from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from llm_service import call_gemini
from dotenv import load_dotenv
import os
app = Flask(__name__)
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
# MongoDB setup (adjust URI and db/collection names as needed)
client = MongoClient(MONGO_URI,tlsAllowInvalidCertificates=True)
db = client[DATABASE_NAME]
mycol = db[COLLECTION_NAME]

print(mycol.find_one())  # Debugging line to check if connection works

def get_article_by_id(article_id):
    try:
        print(ObjectId(article_id))
        article = mycol.find_one({"_id": ObjectId(article_id)})
        print("Article fetched:", article)  # Debugging line
        return article
    except Exception:
        return None

@app.route("/summarize", methods=["POST"])
def summarize_article():
    data = request.get_json()
    article_id = data.get("article_id")
    if not article_id:
        return jsonify({"error": "article_id is required"}), 400

    article = get_article_by_id(article_id)
    if not article:
        return jsonify({"error": f"Article with ID {article_id} not found."}), 404

    # Fetch title and meta description
    title = article.get("title", "")
    meta_desc = article.get("meta", {}).get("description", "")

    # Summarize meta description
    summary_meta = call_gemini("summary", context_vars={"text":title+meta_desc}) if meta_desc else ""

    response = {
        "title": title,
        "summary": summary_meta,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)