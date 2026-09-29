from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=20000)


class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=10000)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return await _safe_call(answer_question, payload.question)


@app.post("/explain")
async def explain(payload: TextRequest):
    return await _safe_call(explain_topic, payload.text)


@app.post("/quiz")
async def quiz(payload: TextRequest):
    return await _safe_call(generate_quiz, payload.text)


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return await _safe_call(summarize_text, payload.text)


@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    return await _safe_call(get_learning_recommendations, payload.text)


async def _safe_call(function, value: str):
    try:
        result = await function(value)
        return {"success": True, "data": result}
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"success": False, "error": str(exc)})
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": f"EduGenie could not complete the request: {exc}"},
        )
