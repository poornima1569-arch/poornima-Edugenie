from gemini_client import generate_text

SYSTEM = """You are EduGenie's learning-path planner. Create practical, age-appropriate educational paths.
Organize from beginner to intermediate to advanced. Include suggested time ranges, practice activities, and resource types.
Do not claim that a specific external resource exists unless you are confident; resource suggestions can be described by type."""


async def get_learning_recommendations(topic: str) -> str:
    return await generate_text(
        f"Create a structured learning path for: {topic}\n\nInclude:\n1. Prerequisites\n2. Beginner topics\n3. Intermediate topics\n4. Advanced topics\n5. Practice projects\n6. A realistic weekly sequence\n7. Resource types for further study.",
        system_instruction=SYSTEM,
        temperature=0.5,
        max_output_tokens=2500,
    )
