def fake_llm(prompt: str):
    # Replace with OpenAI later
    if "score" in prompt.lower():
        return "85"
    return "Generated response"