# from sqlalchemy import Column, Integer, String, Float, Text
# from db import Base

# class Candidate(Base):
#     __tablename__ = "candidates"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     resume_text = Column(Text)
#     ats_score = Column(Float)
#     stage = Column(String)  # ATS, Interview, HR, Scheduled


from sqlalchemy import Column, Integer, String, Float, Text
from db import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    resume_text = Column(Text)
    ats_score = Column(Float)
    stage = Column(String)