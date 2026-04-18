from pydantic import BaseModel

class CandidateCreate(BaseModel):
    name: str
    email: str

class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    ats_score: float
    stage: str

    class Config:
        orm_mode = True