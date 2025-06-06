import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from chatbot_logic import ArticleWriterModule, get_bot_response

app = FastAPI(
    title="Gemini Chatbot API",
    description="An API for a multi-functional chatbot with summarization, Q&A, and an interactive article writer.",
    version="1.0.0"
)

SESSIONS: Dict[str, ArticleWriterModule] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Main endpoint for interacting with the chatbot.
    
    - **session_id**: A unique identifier for the user's conversation.
    - **message**: The user's input message.
    """
    session_id = request.session_id
    user_message = request.message

    if not session_id or not user_message:
        raise HTTPException(status_code=400, detail="session_id and message are required.")

    # Get or create a session for the user
    if session_id not in SESSIONS:
        SESSIONS[session_id] = ArticleWriterModule()
        print(f"New session created: {session_id}")
    
    writer_module = SESSIONS[session_id]

    # Get the bot's response using our core logic
    bot_reply = get_bot_response(user_message, writer_module)
    
    # Optional: Clean up session if the article writing process is finished
    if writer_module.stage == "idle" and "Here is your complete article" in bot_reply:
         del SESSIONS[session_id]
         print(f"Session closed after article generation: {session_id}")

    return ChatResponse(session_id=session_id, response=bot_reply)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gemini Chatbot API. Please use the /docs endpoint to see the API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)