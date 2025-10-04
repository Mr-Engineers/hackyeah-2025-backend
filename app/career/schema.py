from pydantic import BaseModel, Field

class JobRead(BaseModel):
    id: int
    title: str
    company: str
    salary: float
    stress_level: int
    required_education: int
    required_experience: int
    employment_type: str

    class Config:
        from_attributes = True

class JobApplyRequest(BaseModel):
    game_id: int = Field(...)
    job_id: int = Field(...)