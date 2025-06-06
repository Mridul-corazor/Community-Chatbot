# Community-Chatbot

A multi-functional chatbot API for content communities, built in Python. This project provides an intelligent assistant that can:

- **Summarize articles or user-provided content**
- **Suggest new blog topics based on existing articles**
- **Answer questions based on provided content (contextual Q&A)**
- **Guide users through an interactive, multi-step article writing process powered by Google Gemini**

## Features

- **RESTful API**: Exposes endpoints via FastAPI and Flask (choose your preferred framework).
- **Interactive Article Writer**: The chatbot walks users through brainstorming, titling, and drafting a complete article, ensuring high-quality, SEO-friendly output.
- **Summarization & Topic Suggestions**: Quickly get concise summaries or creative new blog ideas from any text.
- **Contextual Q&A**: The bot answers questions using only the supplied article context, avoiding hallucinated answers.
- **Session Management**: Each user session maintains progress for the article-writing workflow.

## Quick Start

### Prerequisites

- Python 3.8+
- A Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mridul-corazor/Community-Chatbot.git
   cd Community-Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Run the API server (FastAPI)**
   ```bash
   uvicorn api:app --reload
   ```
   or **Run the Flask API**
   ```bash
   python flask_api.py
   ```

5. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

## Usage

### Endpoints

- `POST /chat`: Main endpoint to interact with the chatbot.  
  Request body:
  ```json
  {
    "session_id": "unique-session-id",
    "message": "Your message to the bot"
  }
  ```
- `GET /`: Returns a welcome message and API usage hint.

### Example Conversation

1. **User**: "Write a new article."
2. **Bot**: "Great! Let's write an article. First, please tell me: 1. What industry or topic is this for? 2. Who is the target audience?"
3. *(User provides context)*
4. **Bot**: Suggests 5 SEO titles. User picks one.
5. **Bot**: Suggests 5 blog ideas. User picks one.
6. **Bot**: Generates a full article based on selections.

## Project Structure

```
├── api.py              # FastAPI server
├── flask_api.py        # (Alternative) Flask server
├── chatbot_logic.py    # Core logic for intent detection, article writing, etc.
├── llm_service.py      # Integration with Gemini LLM
├── prompts.py          # Prompt templates for LLM
├── config.py           # Loads API keys and model config
├── requirements.txt    # Python dependencies
└── ...
```

## Dependencies

- `google-generativeai`
- `python-dotenv`
- `flask`, `fastapi`, `uvicorn`, `flask-cors`
- `requests`

(See `requirements.txt` for the full list.)

## Contributing

Contributions, issues and feature requests are welcome!  
Feel free to open an issue or submit a pull request.

## License

*No license specified yet. Please add one if you intend to make this project open source.*

---

**Author**: [Mridul-corazor](https://github.com/Mridul-corazor)
