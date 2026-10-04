# 🧞‍♂️ EduGenie: Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students and educators of all academic levels, EduGenie integrates cloud-based Gemini AI models with an intuitive, responsive web interface.

---

## 📌 Features & Modules

1. **Ask EduGenie a Question (`/qa` endpoint)**
   - Answers general knowledge and academic questions concisely and accurately using Google Gemini.
2. **Need an Explanation? (`/explain` endpoint)**
   - Breaks down complex academic concepts into simplified language tailored for school students and beginners.
   - Built to support local instruction-tuned `MBZUAI/LaMini-Flan-T5-783M` with automatic Gemini cloud fallback.
3. **Summarize a Paragraph (`/summarize` endpoint)**
   - Distills long educational passages into concise, easy-to-digest summaries without losing core context.
4. **Generate a Quiz (`/quiz` endpoint)**
   - Automatically crafts 3 multiple-choice questions (MCQs) complete with 4 options and real-time answer verification.
5. **Get Learning Recommendations (`/learn/recommendations` endpoint)**
   - Generates structured, adaptive learning paths with beginner, intermediate, and advanced levels, timelines, and suggested study resources.

---

## 🔑 How to Get a Free Google Gemini API Key

To enable EduGenie's AI capabilities, you need a Google Gemini API key. Follow these simple steps:

### Step 1: Open Google AI Studio
1. Open your browser and go to [https://aistudio.google.com/](https://aistudio.google.com/) (or directly to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)).
2. Sign in with your standard **Google Account**.

### Step 2: Create Your API Key
1. In Google AI Studio, click on the **"Get API key"** button on the left sidebar.
2. Click **"Create API key"**.
3. Choose either:
   - **"Create API key in new project"**, or
   - Select an existing Google Cloud project from the dropdown.
4. A popup will appear displaying your new API key (starts with `AIzaSy...`).
5. Click **Copy** to copy the key to your clipboard.

### Step 3: Add the API Key to EduGenie
You have two convenient ways to use your key:

#### Option A: In the `.env` File (Recommended)
1. Open `EduGenie/.env` in your text editor.
2. Replace `your_gemini_api_key_here` with your copied key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
3. Save the file. The server will automatically use this key.

#### Option B: Directly from the Web Interface
1. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
2. Click the **"Set / Change API Key"** button at the top.
3. Paste your Gemini API key and click **"Save in Browser"**.

---

## 🚀 How to Run EduGenie

### 1. Requirements
- Python 3.10+ (Python 3.11 is installed at `C:\Users\LENOVO\Python311`)
- Dependencies installed from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Start the Server
Run the FastAPI development server using Uvicorn:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Or directly:
```bash
python main.py
```

### 3. Open in Browser
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 📁 Project Architecture

```
EduGenie/
├── main.py                   # FastAPI backend routes & application server
├── qna.py                    # Question-answering logic using Gemini
├── explanation_module.py     # Concept explanation logic (LaMini-Flan-T5 / Gemini)
├── summary_module.py         # Summarization module
├── quiz_module.py            # Quiz generation module with MCQ format
├── learning_path.py          # Adaptive learning path generator
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (Gemini API key)
├── .env.example              # Example environment configuration template
├── templates/
│   └── index.html            # Main HTML UI template
└── static/
    └── style.css             # CSS styling and responsive layout
```

