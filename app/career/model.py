from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    salary = Column(Float)
    stress_level = Column(Integer)
    required_education = Column(Integer)
    required_career_level = Column(Integer)
    employment_type = Column(String)
