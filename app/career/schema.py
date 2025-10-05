from pydantic import BaseModel, Field
from typing import Literal

class JobRead(BaseModel):
    id: int
    title: Literal["Software Engineer"]
    company: str
    salary: float
    stress_level: int = Field(..., ge=0, le=11)
    required_education: Literal[1, 2, 3, 4, 5]
    required_career_level: int = Field(..., ge=0, le=1000)
    employment_type: Literal["Umowa o prace", "Umowa o dzielo", "Umowa zlecenie", "Kontrakt"]
    tier: Literal[1, 2, 3, 4, 5, 6, 7, 8]

    class Config:
        from_attributes = True

class JobOffer(BaseModel):
    job_details: JobRead = Field(...)
    eligible: bool = Field(...)

class JobApplyRequest(BaseModel):
    job_id: int = Field(...)