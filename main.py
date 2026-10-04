import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie: Google Gemini Powered Learning Assistant")

# Base directory for static and template files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)


def extract_api_key(request: Request, body_data: dict = None) -> str:
    """Extracts custom API key from headers or request payload if provided."""
    key = request.headers.get("x-gemini-key")
    if not key and body_data and isinstance(body_data, dict):
        key = body_data.get("api_key")
    return key


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the EduGenie frontend user interface."""
    return templates.TemplateResponse(request=request, name="index.html")


# Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(request: Request, question: str = Query(...)):
    """Handles general and academic queries."""
    key = extract_api_key(request)
    answer = answer_question_with_gemini(question, api_key=key)
    return {"answer": answer}


# Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    """Explains complex concepts in simple terms."""
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    key = extract_api_key(request, data)
    explanation = explain_topic(topic, api_key=key)
    return {"topic": topic, "explanation": explanation}


# Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    """Summarizes lengthy educational text."""
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    key = extract_api_key(request, data)
    summary = summarize_text(text, api_key=key)
    return {"summary": summary}


# Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    """Generates 3 multiple-choice questions from topic or passage."""
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    key = extract_api_key(request, data)
    quiz = generate_quiz(text, api_key=key)
    return JSONResponse(content={"quiz": quiz})


# Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(request: Request, topic: str = Query(...)):
    """Provides a tailored beginner-to-advanced learning path."""
    key = extract_api_key(request)
    recommendation = get_learning_recommendations(topic, api_key=key)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
