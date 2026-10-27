import os

from dotenv import load_dotenv
from openrouter import OpenRouter

# Load environment variables from .env
load_dotenv()


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to OpenRouter and return the generated text."""

    # Reload environment variables to reflect any updates in .env
    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL")

    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Check your .env file."
        )

    if not model:
        raise RuntimeError(
            "OPENROUTER_MODEL is missing. Check your .env file."
        )

    with OpenRouter(api_key=api_key) as client:
        try:
            response = client.chat.send(
                model=model,
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
        except Exception as err:
            # If the configured free model experiences temporary upstream rate limiting,
            # attempt a fallback free model so users are not blocked.
            fallback_model = "nvidia/nemotron-3.5-lightning:free"
            if ("429" in str(err) or "rate" in str(err).lower()) and model != fallback_model:
                response = client.chat.send(
                    model=fallback_model,
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
            else:
                raise err

    result = response.choices[0].message.content

    if not result:
        raise RuntimeError("The AI model returned an empty response.")

    return result