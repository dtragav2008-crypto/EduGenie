import os
from dotenv import load_dotenv
from gemini_client import format_gemini_error, generate_gemini_text

load_dotenv()


def answer_question_with_gemini(question: str, api_key: str = None) -> str:
    """Answers general knowledge and academic questions using Google Gemini."""
    try:
        active_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or active_key.strip() in ["", "your_gemini_api_key_here", "YOUR_GEMINI_API_KEY_HERE"]:
            return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file or click 'Set / Change API Key' in the web interface."

        return generate_gemini_text(question, active_key)
    except Exception as e:
        return f"⚠️ {format_gemini_error(e)}"
