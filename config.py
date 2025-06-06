import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = os.environ["GOOGLE_API_KEY"]
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")
except (KeyError, ValueError) as e:
    print(f"Error configuring Gemini API: {e}")
    exit()

model = genai.GenerativeModel("gemini-2.0-flash")

ARTICLE = """

"""