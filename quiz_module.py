import os
import re
import json
from dotenv import load_dotenv
from gemini_client import generate_gemini_text

load_dotenv()


def clean_json_block(text: str) -> str:
    """Removes markdown code fences and returns clean JSON string."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```\s*$", "", cleaned.strip(), flags=re.MULTILINE)
    return cleaned.strip()


def offline_study_quiz(text: str) -> list:
    subject = " ".join(text.split())[:100] or "this topic"
    questions = [
        {
            "question": f"What is a useful first step when studying {subject}?",
            "options": [
                "Identify the key terms and core ideas",
                "Skip the definitions and start with the hardest detail",
                "Memorize every sentence before understanding it",
                "Use only one example and avoid further practice",
            ],
            "answer": "Identify the key terms and core ideas",
        },
        {
            "question": f"Which activity best checks your understanding of {subject}?",
            "options": [
                "Explain it in your own words and solve a new example",
                "Reread the same paragraph without taking a break",
                "Look only at the answer key",
                "Avoid questions that use unfamiliar examples",
            ],
            "answer": "Explain it in your own words and solve a new example",
        },
        {
            "question": f"If an answer about {subject} seems unexpected, what should you do?",
            "options": [
                "Review the assumptions and each step in your reasoning",
                "Change the answer until it looks familiar",
                "Ignore the result and move to a new subject",
                "Assume the first attempt must be correct",
            ],
            "answer": "Review the assumptions and each step in your reasoning",
        },
    ]
    for question in questions:
        question["offline"] = True
    return questions


def generate_quiz(text: str, api_key: str = None) -> list:
    """Generates 3 multiple-choice questions (MCQs) in JSON format from passage or topic."""
    try:
        active_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or active_key.strip() in ["", "your_gemini_api_key_here", "YOUR_GEMINI_API_KEY_HERE"]:
            return offline_study_quiz(text)

        prompt = f"""You are a quiz generator.

From the following passage or topic, create exactly 3 multiple-choice questions. Each question must include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON only**, with no surrounding text or explanations, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}"""

        response_text = generate_gemini_text(prompt, active_key)
        cleaned = clean_json_block(response_text)

        try:
            quiz_data = json.loads(cleaned)
            if isinstance(quiz_data, list):
                return quiz_data
            elif isinstance(quiz_data, dict) and "quiz" in quiz_data:
                return quiz_data["quiz"]
        except Exception:
            match = re.search(r"\[.*\]", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise

        return [{"error": "Invalid format returned by quiz generator."}]
    except Exception as e:
        return offline_study_quiz(text)
