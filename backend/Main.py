from fastapi import FastAPI
from app.models.resume_input import ResumeInput
from fastapi.middleware.cors import CORSMiddleware
from app.services import resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) 

@app.get("/")
def hello():
    return "Resume Builder Application"


@app.post("/resume")
def generate_resume(resume_input: ResumeInput):
    # Call the generate_resume function from the resume service
    result = resume.generate_resume(resume_input)
    return {"status": "success", "data": result}
