import re
from llm_service import call_gemini
from config import ARTICLE

class ArticleWriterModule:
    """Manages the multi-step process of writing an article."""
    def __init__(self):
        self.stage = "idle"
        self.context = {}

    def reset(self):
        self.stage = "idle"
        self.context = {}

    def handle(self, user_msg: str):
        """Processes user input through the article writing workflow."""
        msg_lower = user_msg.strip().lower()

        if self.stage == "idle":
            if "write" in msg_lower or "new article" in msg_lower:
                self.stage = "awaiting_context"
                return "Great! Let's write an article. First, please tell me: 1. What industry or topic is this for? 2. Who is the target audience?"
            return None # Not handled by this module

        elif self.stage == "awaiting_context":
            self.context["description"] = user_msg
            self.stage = "generating_titles"
            return self._generate_titles()

        elif self.stage == "awaiting_title_choice":
            self.context["chosen_title"] = user_msg
            self.context["title"] = user_msg  # Store title for later use
            self.stage = "generating_blog_ideas"
            return self._generate_blog_ideas()

        elif self.stage == "awaiting_blog_choice":
            self.context["chosen_blog"] = user_msg
            self.stage = "generating_final_article"
            return self._generate_article()

        return None # Should not be reached

    def _generate_titles(self):
        titles = call_gemini("generate_titles", context_vars={"description": self.context["description"]})
        self.context["titles"] = titles
        self.stage = "awaiting_title_choice"
        return f"Here are 5 title options. Please copy and paste the one you'd like to use:\n\n{titles}"

    def _generate_blog_ideas(self):
        ideas = call_gemini("generate_blog_ideas", context_vars=self.context)
        self.context["ideas"] = ideas
        self.stage = "awaiting_blog_choice"
        return f"Excellent. Now, here are 5 blog ideas based on that title. Please pick one to develop:\n\n{ideas}"

    def _generate_article(self):
        article = call_gemini("generate_article", context_vars=self.context)
        final_response = f"**Here is your complete article:**\n\n---\n\n{article}"
        self.reset() # Reset for the next use
        return final_response

# === Intent Detection ===
def detect_intent(msg: str):
    msg_lower = msg.lower()
    if "summary" in msg_lower or "summarize" in msg_lower: return "summary"
    if "topic" in msg_lower or "suggest" in msg_lower: return "topic"
    return "qa" # Default fallback

# === Main Chat Engine Function ===
def get_bot_response(user_msg: str, writer_module: ArticleWriterModule) -> str:
    """
    Determines the user's intent and gets the appropriate response.
    This is the main entry point for the logic.
    """
    # First, check for simple greetings
    if re.match(r"^\s*(hi|hello|hey)\b.*", user_msg.lower()):
        return "Hi there! How can I help you today? You can ask me to summarize the article, suggest new topics, ask a question about it, or write a new article."

    # Second, let the ArticleWriterModule try to handle it
    module_response = writer_module.handle(user_msg)
    if module_response:
        return module_response

    # If not handled, fall back to simple intent detection
    intent = detect_intent(user_msg)
    
    if intent == "summary":
        return call_gemini("summary", context_vars={"text": ARTICLE})
    elif intent == "topic":
        return call_gemini("suggest_topics", context_vars={"text": ARTICLE})
    else: # Default to Q&A
        return call_gemini("question_answering", context_vars={"text": ARTICLE, "question": user_msg})