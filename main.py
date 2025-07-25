from fastapi import FastAPI, Request
from pydantic import BaseModel
from interview_engine import InterviewEngine

app = FastAPI()
engine = InterviewEngine()

class UserMessage(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat(msg: UserMessage):
    response = await engine.handle_message(msg.session_id, msg.message)
    return {"response": response}
