import os
from functools import lru_cache

from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@lru_cache(maxsize=1)
def get_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google Gemini API key."
        )
    return genai.Client(api_key=api_key)


async def generate_text(prompt: str, *, system_instruction: str | None = None, temperature: float = 0.4, max_output_tokens: int = 2048) -> str:
    client = get_client()
    from google.genai import types
    from google.genai import types
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


async def generate_json(prompt: str, schema: dict, *, system_instruction: str | None = None) -> str:
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=4096,
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=schema,
    )
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned empty JSON output.")
    return text
