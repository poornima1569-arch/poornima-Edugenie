import os
from functools import lru_cache

from gemini_client import generate_text

LOCAL_MODEL_NAME = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
ENABLE_LOCAL_MODEL = os.getenv("ENABLE_LOCAL_MODEL", "false").lower() == "true"


@lru_cache(maxsize=1)
def _load_local_model():
    if not ENABLE_LOCAL_MODEL:
        return None
    from transformers import pipeline
    return pipeline("text2text-generation", model=LOCAL_MODEL_NAME, device=-1)


async def explain_topic(topic: str) -> str:
    """Explain a concept simply. The documented LaMini model is optional and lazy-loaded.

    Keeping it disabled by default avoids a large first-run model download. Gemini remains the
    reliable cloud path unless ENABLE_LOCAL_MODEL=true is explicitly configured.
    """
    if ENABLE_LOCAL_MODEL:
        generator = _load_local_model()
        if generator is not None:
            result = generator(
                f"Explain this educational concept in simple language with one example: {topic}",
                max_new_tokens=220,
                do_sample=False,
            )
            if result and result[0].get("generated_text"):
                return result[0]["generated_text"].strip()

    return await generate_text(
        f"Explain the following concept for a beginner. Use simple words, a short step-by-step explanation, and one example.\n\nConcept: {topic}",
        system_instruction="You are EduGenie's concept explanation tutor. Prefer clarity over jargon.",
        temperature=0.3,
    )
