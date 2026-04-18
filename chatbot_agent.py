def chatbot(query: str):
    if "candidates" in query.lower():
        return "Fetching candidates..."
    elif "schedule" in query.lower():
        return "Scheduling candidate..."
    return "Unknown query"