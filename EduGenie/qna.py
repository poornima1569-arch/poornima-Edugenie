from gemini_client import generate_text

SYSTEM = """You are EduGenie, a patient educational assistant. Answer academic questions accurately and concisely.
Explain unfamiliar terms briefly, use simple language, and say when a question is ambiguous or requires verification.
Do not invent sources or facts."""


async def answer_question(question: str) -> str:
    return await generate_text(
        f"Answer this student's question. Give the direct answer first, then a short explanation if useful.\n\nQuestion: {question}",
        system_instruction=SYSTEM,
        temperature=0.3,
    )
