import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to Google Gemini API and return the generated text."""

    # Reload environment variables to reflect any updates in .env
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_MODEL") or "gemini-3.5-flash"

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
    except Exception as err:
        # Fallback to verified active model gemini-3.1-flash-lite if the primary model encounters temporary unavailability
        fallback_model = "gemini-3.1-flash-lite"
        if model != fallback_model:
            response = client.models.generate_content(
                model=fallback_model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )
        else:
            raise err

    result = response.text

    if not result:
        raise RuntimeError("The AI model returned an empty response.")

    return result