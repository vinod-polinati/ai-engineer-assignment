from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from interview_engine import InterviewEngine
import os
from datetime import datetime

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

@app.get("/download-transcript/{session_id}")
async def download_transcript(session_id: str):
    """Download the PDF transcript for a given session"""
    try:
        # Look for the most recent PDF file for this session
        transcripts_dir = "transcripts"
        if not os.path.exists(transcripts_dir):
            raise HTTPException(status_code=404, detail="No transcripts found")
        
        # Find the PDF file for this session
        pdf_files = []
        for filename in os.listdir(transcripts_dir):
            if filename.startswith(session_id) and filename.endswith('.pdf'):
                pdf_files.append(filename)
        
        if not pdf_files:
            raise HTTPException(status_code=404, detail="Transcript not found")
        
        # Get the most recent file
        latest_file = sorted(pdf_files)[-1]
        file_path = os.path.join(transcripts_dir, latest_file)
        
        # Return the PDF file
        return FileResponse(
            path=file_path,
            filename=f"excel_interview_transcript_{session_id}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading transcript: {str(e)}")
