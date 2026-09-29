import json

from pydantic import BaseModel, Field, ValidationError

from gemini_client import generate_json


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "string"}},
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": ["question", "options", "correct_answer", "explanation"],
            },
        }
    },
    "required": ["questions"],
}


async def generate_quiz(text: str) -> dict:
    prompt = f"""Create exactly three multiple-choice questions from the educational content below.
Each question must have exactly four options. The correct_answer must exactly match one option.
Make distractors plausible but clearly incorrect when the content is understood.
Return only the requested JSON structure.

CONTENT:\n{text}"""
    raw = await generate_json(prompt, QUIZ_SCHEMA, system_instruction="You generate reliable educational MCQs.")
    try:
        parsed = QuizResponse.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(f"Quiz response validation failed: {exc}") from exc
    return parsed.model_dump()
