from utils import fake_llm

def hr_questions(resume):
    return fake_llm(f"Ask HR questions for: {resume}")

def evaluate_hr(answer):
    return "HR Score: 80"