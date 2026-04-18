# from langgraph.graph import StateGraph, END
# from typing import TypedDict
# from services.llm import get_llm_response


# class InterviewState(TypedDict):
#     role: str
#     level: str
#     question: str
#     answer: str
#     score: int
#     feedback: str


# # ✅ Generate Question
# async def generate_question(state: InterviewState):
#     prompt = f"""
#     Generate ONE technical interview question for a {state['level']} {state['role']}.

#     Only return the question.
#     """

#     question = await get_llm_response(prompt)

#     return {"question": question}


# # ✅ Evaluate Answer
# async def evaluate_answer(state: InterviewState):
#     prompt = f"""
#     Question: {state['question']}

#     Answer: {state['answer']}

#     Give:
#     Score (0-10)
#     Feedback (1-2 lines)

#     Format:
#     Score: X
#     Feedback: ...
#     """

#     result = await get_llm_response(prompt)

#     try:
#         score = int("".join(filter(str.isdigit, result))) or 5
#     except:
#         score = 5

#     return {
#         "score": score,
#         "feedback": result
#     }


# # ✅ Graph
# def build_interview_graph():
#     graph = StateGraph(InterviewState)

#     graph.add_node("generate", generate_question)
#     graph.add_node("evaluate", evaluate_answer)

#     graph.set_entry_point("generate")

#     graph.add_edge("generate", "evaluate")
#     graph.add_edge("evaluate", END)

#     return graph.compile()


from fastapi import WebSocket

questions = [
    "What is OOP?",
    "Explain REST API",
    "What is SQL JOIN?",
    "Explain async programming",
    "What is React?"
]

async def interview_socket(ws: WebSocket):
    await ws.accept()

    for q in questions:
        await ws.send_text(q)
        ans = await ws.receive_text()

        score = f"Score: {len(ans) % 10}/10"
        await ws.send_text(score)

    await ws.send_text("Interview Completed")