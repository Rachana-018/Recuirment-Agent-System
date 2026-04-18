# from fastapi import FastAPI, Depends, File, Form, UploadFile
# from sqlalchemy.ext.asyncio import AsyncSession
# from db import AsyncSessionLocal, engine
# from models import Base, Candidate
# from agents.ats_agent import build_ats_graph
# import PyPDF2
# import io

# app = FastAPI()

# ats_graph = build_ats_graph()

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # for development
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# from agents.interview_agent import build_interview_graph

# interview_graph = build_interview_graph()


# from pydantic import BaseModel

# class InterviewInput(BaseModel):
#     role: str
#     level: str

# @app.post("/start-interview")
# async def start_interview(data: InterviewInput):
#     result = await interview_graph.ainvoke({
#         "role": data.role,
#         "level": data.level,
#         "question": "",  
#         "answer": ""      
#     })

#     return {
#         "question": result["question"]
#     }

# class AnswerInput(BaseModel):
#     question: str
#     answer: str

# @app.post("/submit-answer")
# async def submit_answer(data: AnswerInput):
#     result = await interview_graph.ainvoke({
#         "role": "",
#         "level": "",
#         "question": data.question,
#         "answer": data.answer
#     })

#     return {
#         "score": result["score"],
#         "feedback": result["feedback"]
#     }


# from fastapi import WebSocket
# import asyncio


# @app.websocket("/ws/interview")
# async def interview_timer(websocket: WebSocket):
#     await websocket.accept()

#     for i in range(30, 0, -1):
#         await websocket.send_text(str(i))
#         await asyncio.sleep(1)

#     await websocket.send_text("TIME_UP")
#     await websocket.close()

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session


# @app.post("/upload-resume")
# async def upload_resume(
#     name: str = Form(...),
#     email: str = Form(...),
#     job_description: str = Form(...),
#     file: UploadFile = File(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     try:
#         pdf_bytes = await file.read()

#         # Extract text safely
#         pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
#         resume_text = ""

#         for page in pdf_reader.pages:
#             text = page.extract_text()
#             if text:
#                 resume_text += text

#         if not resume_text.strip():
#             return {"error": "Could not extract text from PDF"}

#         # Call ATS
#         result = await ats_graph.ainvoke({
#             "resume": resume_text,
#             "job_description": job_description
#         })

#         candidate = Candidate(
#             name=name,
#             email=email,
#             resume_text=resume_text,
#             role_applied="Software Engineer",
#             stage=result.get("decision", "Unknown"),
#             ats_score=result.get("score", 0)
#         )

#         db.add(candidate)
#         await db.commit()

#         return {
#             "score": result.get("score"),
#             "decision": result.get("decision")
#         }

#     except Exception as e:
#         print("🔥 ERROR:", str(e))  # check terminal
#         return {"error": str(e)}


from fastapi import FastAPI, UploadFile, WebSocket
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import Candidate
from agents.ats_agent import run_ats
from agents.interview_agent import interview_socket
from agents.scheduler_agent import schedule

Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Upload Resume
@app.post("/upload/")
async def upload_resume(file: UploadFile):
    content = await file.read()
    result = await run_ats(content)
    return result



# Save Candidate
@app.post("/candidate/")
def create_candidate(name: str, email: str):
    db: Session = SessionLocal()

    candidate = Candidate(
        name=name,
        email=email,
        ats_score=0,
        stage="Applied"
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate

# Get Candidates
@app.get("/candidates/")
def get_candidates():
    db: Session = SessionLocal()
    return db.query(Candidate).all()

# WebSocket Interview
@app.websocket("/ws/interview")
async def websocket_endpoint(ws: WebSocket):
    await interview_socket(ws)

# Schedule Interview
@app.post("/schedule/")
async def schedule_interview(email: str):
    return await schedule(email)