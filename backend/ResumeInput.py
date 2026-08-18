from typing import Optional

from pydantic import BaseModel

class ResumeInput(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    jobRole: str
    skills: str
    experience: str
    projects: str
    education: str
    skills: Optional[str] = ""
    certifications: Optional[str] = ""
