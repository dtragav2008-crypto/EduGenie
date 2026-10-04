import os
from dotenv import load_dotenv
from gemini_client import format_gemini_error, generate_gemini_text

load_dotenv()


def summarize_text(text: str, api_key: str = None) -> str:
    """Summarizes text into concise, easy-to-understand versions retaining core points."""
    try:
        active_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or active_key.strip() in ["", "your_gemini_api_key_here", "YOUR_GEMINI_API_KEY_HERE"]:
            return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file or click 'Set / Change API Key' in the web interface."

        prompt = f"Summarize the following text in simple language:\n\n{text}"
        return generate_gemini_text(prompt, active_key)
    except Exception as e:
        return f"⚠️ {format_gemini_error(e)}"
