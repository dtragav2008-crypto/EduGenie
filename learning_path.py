import os
import html
from dotenv import load_dotenv
from gemini_client import format_gemini_error, generate_gemini_text

load_dotenv()


def _offline_learning_path(topic: str, reason: str) -> str:
    safe_topic = html.escape(topic.strip())
    return f"""### Offline starter path: {safe_topic}

Gemini is unavailable, so this is a general plan to get started. Retry later for AI-tailored recommendations. {reason}

**Beginner**
- Write down what you already know about {safe_topic} and list unfamiliar terms.
- Find an introductory lesson that defines the core ideas; summarize each idea in your own words.
- Work through one simple example and explain why each step makes sense.

**Intermediate**
- Break {safe_topic} into three to five subtopics and study them in prerequisite order.
- Complete a worked example, then solve a similar problem without looking at the solution.
- Compare two approaches or examples and note when each is useful.

**Advanced**
- Explore assumptions, edge cases, and current applications of {safe_topic}.
- Build a small project or solve a realistic problem, documenting your reasoning.
- Review mistakes, revisit weak subtopics, and explain the complete topic from memory.

**Check your progress**
- Can you define the key terms and explain the main idea without notes?
- Can you solve a new example and justify your choices?
- Can you identify what you still need to learn next?

**Find resources**
- Search for "{safe_topic} beginner introduction" for a first lesson.
- Search for "{safe_topic} worked examples" for practice.
- For advanced study, look for university course notes, textbooks, or official documentation related to the topic.
"""


def get_learning_recommendations(topic: str, api_key: str = None) -> str:
    """Generates a structured, adaptive learning path with beginner, intermediate, and advanced levels."""
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, books).
Include beginner, intermediate, and advanced levels if needed."""

    try:
        active_key = api_key or os.getenv("GEMINI_API_KEY")
        if not active_key or active_key.strip() in ["", "your_gemini_api_key_here", "YOUR_GEMINI_API_KEY_HERE"]:
            reason = "No Gemini API key is configured."
            return _offline_learning_path(topic, reason)

        return generate_gemini_text(prompt, active_key)
    except Exception as e:
        return _offline_learning_path(topic, format_gemini_error(e))
