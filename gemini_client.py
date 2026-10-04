import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAMES = ("gemini-3.1-flash-lite", "gemini-3.8-flash")


def generate_gemini_text(prompt: str, api_key: str) -> str:
    """Generate text with the configured Gemini model."""
    client = genai.Client(
        api_key=api_key.strip(),
        http_options=types.HttpOptions(
            timeout=10000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    last_error = None
    for model_name in MODEL_NAMES:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            text = response.text
            if text:
                return text.strip()
            last_error = RuntimeError(f"Gemini returned an empty response from {model_name}.")
        except Exception as error:
            last_error = error
            details = str(error).lower()
            if not any(marker in details for marker in ("503", "504", "unavailable", "deadline", "timeout", "timed out")):
                raise

    raise last_error or RuntimeError("No Gemini model returned a response.")


def format_gemini_error(error: Exception) -> str:
    """Return a concise message for known Gemini service failures."""
    details = str(error)
    if "quota" in details.lower() or "resource_exhausted" in details.lower():
        return "Gemini API quota exceeded. Check usage and billing at https://ai.google.dev/gemini-api/docs/rate-limits."
    if "timeout" in details.lower() or "timed out" in details.lower():
        return "Gemini took too long to respond. Please try again shortly."
    return f"Gemini request failed: {details}"
