# from langgraph.graph import StateGraph, END
# from typing import TypedDict
# from services.llm import get_llm_response


# class ATSState(TypedDict):
#     resume: str
#     job_description: str
#     score: int
#     decision: str



# async def score_resume(state: ATSState):
#     prompt = f"""
#     Evaluate the resume against the job description.

#     Resume:
#     {state['resume']}

#     Job Description:
#     {state['job_description']}

#     Give ONLY a score from 0 to 100.
#     """

#     result = await get_llm_response(prompt)

#     try:
#         score = int("".join(filter(str.isdigit, result)))
#     except:
#         score = 50

#     return {"score": score}



# def decide(state: ATSState):
#     if state["score"] >= 80:
#         return {"decision": "INTERVIEW"}
#     else:
#         return {"decision": "REJECT"}



# def build_ats_graph():
#     graph = StateGraph(ATSState)

#     graph.add_node("score", score_resume)
#     graph.add_node("decision", decide)

#     graph.set_entry_point("score")

#     graph.add_edge("score", "decision")
#     graph.add_edge("decision", END)

#     return graph.compile()

 
from langgraph.graph import StateGraph
from typing import TypedDict
from utils import fake_llm

class ATSState(TypedDict):
    resume: str
    score: float
    decision: str

def parse_resume(state):
    return {"resume": state["resume"].decode("utf-8")}

def score_resume(state):
    score = fake_llm(f"Score this resume: {state['resume']}")
    return {"score": float(score)}

def decision_node(state):
    return {
        "decision": "Proceed" if state["score"] >= 80 else "Reject"
    }

def build_graph():
    graph = StateGraph(ATSState)

    graph.add_node("parse", parse_resume)
    graph.add_node("score", score_resume)
    graph.add_node("decision", decision_node)

    graph.set_entry_point("parse")
    graph.add_edge("parse", "score")
    graph.add_edge("score", "decision")

    return graph.compile()

async def run_ats(resume):
    graph = build_graph()
    return await graph.ainvoke({"resume": resume})