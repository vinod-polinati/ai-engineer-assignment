# AI-Powered Excel Mock Interviewer  

## 1. Problem Statement

Manual Excel interviews are a bottleneck in our hiring process, causing delays and inconsistent candidate evaluations. We need an automated, scalable, and fair way to assess Excel skills for Finance, Operations, and Data Analytics roles.

## 2. Solution Overview

I built an AI-powered web app that simulates a real Excel interview. The system consists of a FastAPI backend for interview logic and a React frontend for the user interface. The system asks warm-up and technical questions, evaluates answers using a large language model (LLM), and provides a detailed feedback report with automatic PDF transcript generation. The goal is to save time for senior analysts and ensure consistent, unbiased candidate assessment.

## 3. System Architecture
```
flowchart TD
    A[User (Candidate)] -- Chat UI --> B[React Frontend (frontend-react/)]
    B -- HTTP Requests --> C[FastAPI Backend (main.py)]
    C -- Interview Logic --> D[Interview Engine (interview_engine.py)]
    D -- LLM API Calls --> E[Groq API]
    D -- Save Transcript --> F[PDF Files]
```
- **React Frontend (`frontend-react/`):** Modern, minimal dark-mode chat interface built with React and TypeScript.
- **FastAPI Backend (`main.py`):** RESTful API that handles chat requests and manages interview sessions with robust error handling.
- **Interview Engine (`interview_engine.py`):** Core interview logic, question flow, answer evaluation, and transcript generation.
- **LLM Service (`llm_service.py`):** Handles communication with the Groq API for answer evaluation and feedback generation.
- **PDF Transcript Storage:** Interview transcripts are automatically saved as PDF files with comprehensive error handling and fallback mechanisms.

## 4. Interview Flow

1. **Introduction:** The bot introduces itself and explains the process.
2. **Warm-up:** Asks 2–3 general questions to get the candidate comfortable.
3. **Technical Questions:** Asks a series of Excel-related questions.
4. **Clarification:** If the candidate is confused, the bot provides hints (not answers).
5. **Evaluation:** Each answer is scored and explained by the LLM.
6. **Summary:** At the end, the bot gives a feedback report (strengths, weaknesses, overall impression).
7. **PDF Transcript:** The full interview is automatically saved as a PDF file with bulletproof error handling.

## 5. Technology Stack & Justification

- **FastAPI:**  
  *Provides a robust, high-performance backend API with automatic documentation and type validation. Handles concurrent requests efficiently with comprehensive error handling.*
- **React + TypeScript:**  
  *Modern, responsive frontend with type safety and excellent developer experience. Minimal dark-mode design for professional appearance.*
- **LLM Provider:** Groq API (Llama-3)  
  *Provides high-quality language understanding and generation for answer evaluation and feedback. The API key is managed securely using environment variables.*
- **PDF Generation:** FPDF  
  *Automatically generates professional PDF transcripts of each interview session with robust error handling and fallback mechanisms.*

## 6. Key Features

- **Modern Chat Interface:** Clean, minimal dark-mode React frontend with real-time messaging.
- **Conversational AI:** Simulates a real interview with multi-turn dialogue.
- **Dynamic Evaluation:** Uses LLM to score and explain answers.
- **Clarification:** Detects confusion and provides hints.
- **Session Management:** Each interview is tracked by a unique session ID.
- **Feedback Report:** Summarizes candidate performance at the end.
- **Automatic PDF Generation:** All interviews are automatically saved as PDF transcripts with bulletproof error handling.
- **Restart Functionality:** Users can restart the interview at any time.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.
- **Robust Error Handling:** Comprehensive error handling prevents crashes and ensures smooth user experience.
- **Production Ready:** Successfully deployed and tested in production environment.

## 7. Project Structure

```
ai-engineer-assignment/
├── main.py                 # FastAPI backend server with CORS support
├── frontend.py             # Legacy Streamlit frontend (optional)
├── interview_engine.py     # Core interview logic with error handling
├── llm_service.py          # LLM API communication
├── prompts.py              # Interview questions and prompts (ASCII-safe)
├── save_transcript.py      # Bulletproof PDF transcript generation
├── requirements.txt        # Python dependencies including FPDF
├── transcripts/            # Saved PDF interview transcripts
├── frontend-react/         # React frontend application
│   ├── src/
│   │   ├── App.tsx         # Main React component with error handling
│   │   ├── App.css         # Dark mode styling
│   │   └── index.tsx       # React entry point
│   ├── package.json        # Node.js dependencies with proxy config
│   └── README.md           # Frontend documentation
└── Readme.md              # This documentation
```

## 8. Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API key

### Backend Setup
1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```
4. Start the FastAPI backend:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Navigate to the React frontend directory:
   ```bash
   cd frontend-react
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```
4. Open [http://localhost:3000](http://localhost:3000) to view the application.

## 9. Usage

1. The React frontend will automatically connect to your FastAPI backend
2. Type your responses in the input field and press Enter or click Send
3. The AI interviewer will guide you through the Excel interview process
4. Use the "Restart Interview" button to start a new session
5. PDF transcripts are automatically generated and saved in the `transcripts/` directory
6. The system handles errors gracefully and provides detailed feedback

## 10. Production Deployment

### Current Deployment
- **Backend:** Successfully deployed on Render.com at `https://ai-engineer-assignment.onrender.com`
- **Frontend:** Successfully deployed on vercel.com at `https://ai-engineer-assignment.vercel.app/`
- **CORS:** Configured to allow cross-origin requests from frontend domains
- **Error Handling:** Production-ready with comprehensive error handling and logging

## 11. Error Handling & Reliability

### Robust Error Handling
- **PDF Generation:** Non-blocking with comprehensive fallback mechanisms
- **API Communication:** Timeout handling and detailed error logging
- **Text Sanitization:** Automatic removal of non-ASCII characters
- **Graceful Degradation:** System continues working even if non-critical features fail

### Production Features
- **CORS Support:** Configured for cross-origin requests
- **Session Management:** Unique session IDs for each interview
- **Logging:** Comprehensive error logging for debugging
- **Fallback Mechanisms:** Text file generation if PDF fails

## 12. Cold Start & Improvement Plan

- **Cold Start:**  
  The system does not require any pre-existing dataset. It uses LLMs, which are already trained on general Excel knowledge.
- **Improvement Plan:**  
  - Collect transcripts from real candidate sessions (with consent).
  - Analyze common mistakes and add more targeted questions.
  - Fine-tune the LLM or build a custom evaluation model using collected data.
  - Add more advanced Excel scenarios (e.g., file uploads, formula debugging).
  - Implement user authentication and persistent session storage.
  - Add admin dashboard for interview analytics.
  - Implement real-time collaboration features.
  - Add video/audio interview capabilities.

## 13. Limitations & Future Work

- **No user authentication** (MVP only).
- **Session state is in-memory** and not persistent across server restarts.
- **LLM cost and latency** (depends on API provider).
- **No database integration** for persistent storage.

--- 
