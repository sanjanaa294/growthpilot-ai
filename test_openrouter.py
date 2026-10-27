from llm import generate_text


def main():
    print("Testing GrowthPilot AI connection to OpenRouter...\n")

    try:
        answer = generate_text(
            system_prompt=(
                "You are a helpful AI business assistant. "
                "Give clear and concise answers."
            ),
            user_prompt=(
                "In two sentences, explain how AI can help a small "
                "business identify potential customers."
            ),
        )

        print("SUCCESS! OpenRouter returned a response.\n")
        print("AI Response:")
        print(answer)

    except Exception as error:
        print("CONNECTION TEST FAILED")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()