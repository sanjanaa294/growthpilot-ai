import os

from dotenv import load_dotenv
from openrouter import OpenRouter

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to OpenRouter and return the generated text."""

    if not API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Check your .env file."
        )

    if not MODEL:
        raise RuntimeError(
            "OPENROUTER_MODEL is missing. Check your .env file."
        )

    with OpenRouter(api_key=API_KEY) as client:
        response = client.chat.send(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

    result = response.choices[0].message.content

    if not result:
        raise RuntimeError("The AI model returned an empty response.")

    return result