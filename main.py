from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from interview_engine import InterviewEngine

# Initialize FastAPI app and interview engine
app = FastAPI()
engine = InterviewEngine()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        "https://*.netlify.app",  # Netlify deployments
        "*"  # Allow all origins for now (you can restrict this later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic model for user message
class UserMessage(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat(msg: UserMessage):
    response = await engine.handle_message(msg.session_id, msg.message)
    return {"response": response}
