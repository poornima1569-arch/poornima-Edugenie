# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project document. It provides:

- **Q&A** — `/qa`
- **Concept explanation** — `/explain`
- **3-question MCQ quiz** — `/quiz`
- **Summarization** — `/summarize`
- **Personalized learning path** — `/learn/recommendations`

The supplied document describes Gemini 1.5 Pro for cloud tasks and LaMini-Flan-T5-783M locally for explanations. The implementation preserves those module responsibilities, but uses Google's current `google-genai` SDK and makes the LaMini model optional/lazy-loaded. This avoids forcing a large model download during the normal first run.

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## 1. Prerequisites

- Python 3.10 or newer
- VS Code
- A Gemini API key

## 2. Open in VS Code

1. Extract/open the `EduGenie` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and replace the placeholder API key:

```text
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
ENABLE_LOCAL_MODEL=false
```

Keep `.env` private and do not commit it to Git.

## 4. Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## 5. Test

Run the automated tests in a second terminal with the virtual environment activated:

```bash
pytest -q
```

Then manually test the UI:

1. Ask: `What is photosynthesis?`
2. Explain: `Explain binary search for a beginner.`
3. Quiz: paste a paragraph or topic and click Generate.
4. Summarize: paste class notes.
5. Learning path: `SQL`.

## 6. API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"What is a database?"}'
```

### Explain

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain photosynthesis simply."}'
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"Python is a high-level programming language used for web development, automation, data analysis and AI."}'
```

## 7. Optional local LaMini explanation model

The supplied document specifies LaMini-Flan-T5-783M for the explanation module. To enable it:

```text
ENABLE_LOCAL_MODEL=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first explanation request will download/load the model. CPU inference can be considerably slower than Gemini. If you leave the setting `false`, the explanation module uses Gemini instead and the rest of the application remains unchanged.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure the file is named exactly `.env`, is in the project root beside `main.py`, and contains a valid key.

### Model not found / unavailable

Set `GEMINI_MODEL` in `.env` to a Gemini text model available to your API account.

### PowerShell blocks activation

You can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### Port 8000 is busy

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.
