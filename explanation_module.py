import os
from dotenv import load_dotenv
from gemini_client import format_gemini_error, generate_gemini_text

load_dotenv()

explain_tokenizer = None
explain_model = None
local_model_loaded = False
local_model_attempted = False


def load_local_model():
    """Lazily loads local LaMini-Flan-T5 model as specified in EduGenie Milestone 2."""
    global explain_tokenizer, explain_model, local_model_loaded, local_model_attempted
    if local_model_attempted:
        return local_model_loaded

    local_model_attempted = True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        model_name = "MBZUAI/LaMini-Flan-T5-783M"
        explain_tokenizer = AutoTokenizer.from_pretrained(model_name)
        explain_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        local_model_loaded = True
    except Exception as e:
        local_model_loaded = False

    return local_model_loaded


def explain_topic(topic: str, api_key: str = None) -> str:
    """Explains a topic in simple terms using local model or Gemini fallback."""
    # 1. Try local LaMini-Flan-T5 model
    if load_local_model() and explain_tokenizer and explain_model:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            return explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception:
            pass

    # 2. Gemini fallback
    try:
        active_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or active_key.strip() in ["", "your_gemini_api_key_here", "YOUR_GEMINI_API_KEY_HERE"]:
            return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file or click 'Set / Change API Key' in the web interface."

        prompt = (
            f"Explain the concept of '{topic}' in a simple, engaging, and clear way for a school student. "
            f"Use clear everyday analogies and keep the explanation accessible."
        )

        return generate_gemini_text(prompt, active_key)
    except Exception as e:
        return f"⚠️ {format_gemini_error(e)}"
