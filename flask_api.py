from flask import Flask, request, jsonify
from chatbot_logic import ArticleWriterModule, get_bot_response

app = Flask(__name__)

SESSIONS = {}

@app.route("/chat", methods=["POST"])
def chat_with_bot():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message")
    text = data.get("text","")
    if not session_id or not user_message:
        return jsonify({"detail": "session_id and message are required."}), 400

    # Get or create a session for the user
    if session_id not in SESSIONS:
        SESSIONS[session_id] = ArticleWriterModule()
        print(f"New session created: {session_id}")

    writer_module = SESSIONS[session_id]

    # Get the bot's response using our core logic
    bot_reply = get_bot_response(user_message, text, writer_module)

    # Optional: Clean up session if the article writing process is finished
    if writer_module.stage == "idle" and "Here is your complete article" in bot_reply:
        del SESSIONS[session_id]
        print(f"Session closed after article generation: {session_id}")
        
    return jsonify({"session_id": session_id, "response": bot_reply})

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "Welcome to the Gemini Chatbot API. Please use the /docs endpoint to see the API documentation."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)