from gemini_client import generate_text

SYSTEM = """You are EduGenie's summarization module. Summarize educational material faithfully.
Keep important definitions, facts, relationships, and conclusions. Use clear language and bullet points when useful.
Never add information that is not supported by the supplied text."""


async def summarize_text(text: str) -> str:
    return await generate_text(
        f"Summarize the following educational passage for quick revision. Preserve its core meaning and important details.\n\nPASSAGE:\n{text}",
        system_instruction=SYSTEM,
        temperature=0.2,
        max_output_tokens=1800,
    )
