# AI-Powered Excel Mock Interviewer  
**Design Document**

## 1. Problem Statement

Manual Excel interviews are a bottleneck in our hiring process, causing delays and inconsistent candidate evaluations. We need an automated, scalable, and fair way to assess Excel skills for Finance, Operations, and Data Analytics roles.

## 2. Solution Overview

I built an AI-powered web app that simulates a real Excel interview. The system consists of a FastAPI backend for interview logic and a Streamlit frontend for the user interface. The system asks warm-up and technical questions, evaluates answers using a large language model (LLM), and provides a detailed feedback report. The goal is to save time for senior analysts and ensure consistent, unbiased candidate assessment.

## 3. System Architecture
```
flowchart TD
    A[User (Candidate)] -- Chat UI --> B[Streamlit Frontend (frontend.py)]
    B -- HTTP Requests --> C[FastAPI Backend (main.py)]
    C -- Interview Logic --> D[Interview Engine (interview_engine.py)]
    D -- LLM API Calls --> E[Groq API]
    D -- Save Transcript --> F[Local File System]
```
- **Streamlit Frontend (`frontend.py`):** Provides a user-friendly chat interface with session management and restart functionality.
- **FastAPI Backend (`main.py`):** RESTful API that handles chat requests and manages interview sessions.
- **Interview Engine (`interview_engine.py`):** Core interview logic, question flow, answer evaluation, and transcript generation.
- **LLM Service (`llm_service.py`):** Handles communication with the Groq API for answer evaluation and feedback generation.
- **Transcript Storage:** Interview transcripts are saved locally with unique session IDs.

## 4. Interview Flow

1. **Introduction:** The bot introduces itself and explains the process.
2. **Warm-up:** Asks 2–3 general questions to get the candidate comfortable.
3. **Technical Questions:** Asks a series of Excel-related questions.
4. **Clarification:** If the candidate is confused, the bot provides hints (not answers).
5. **Evaluation:** Each answer is scored and explained by the LLM.
6. **Summary:** At the end, the bot gives a feedback report (strengths, weaknesses, overall impression).
7. **Transcript:** The full interview is automatically saved to the local file system.

## 5. Technology Stack & Justification

- **FastAPI:**  
  *Provides a robust, high-performance backend API with automatic documentation and type validation. Handles concurrent requests efficiently.*
- **Streamlit:**  
  *Offers a user-friendly chat interface with built-in session management and easy deployment options.*
- **LLM Provider:** Groq API (Llama-3)  
  *Provides high-quality language understanding and generation for answer evaluation and feedback. The API key is managed securely using environment variables.*
- **Transcript Storage:** Local file system  
  *Interview transcripts are automatically saved with unique session IDs for record-keeping and analysis.*

## 6. Key Features

- **Conversational AI:** Simulates a real interview with multi-turn dialogue.
- **Dynamic Evaluation:** Uses LLM to score and explain answers.
- **Clarification:** Detects confusion and provides hints.
- **Session Management:** Each interview is tracked by a unique session ID.
- **Feedback Report:** Summarizes candidate performance at the end.
- **Automatic Transcript Saving:** All interviews are automatically saved for transparency and analysis.
- **Restart Functionality:** Users can restart the interview at any time.

## 7. Project Structure

```
ai-engineer-assignment/
├── main.py                 # FastAPI backend server
├── frontend.py             # Streamlit frontend interface
├── interview_engine.py     # Core interview logic
├── llm_service.py          # LLM API communication
├── prompts.py              # Interview questions and prompts
├── save_transcript.py      # Transcript saving functionality
├── requirements.txt        # Python dependencies
├── transcripts/            # Saved interview transcripts
└── Readme.md              # This documentation
```

## 8. Setup and Installation

### Prerequisites
- Python 3.8+
- Groq API key

### Installation Steps
1. Clone the repository
2. Install dependencies:
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
5. Start the Streamlit frontend (in a new terminal):
   ```bash
   streamlit run frontend.py
   ```

## 9. Cold Start & Improvement Plan

- **Cold Start:**  
  The system does not require any pre-existing dataset. It uses LLMs, which are already trained on general Excel knowledge.
- **Improvement Plan:**  
  - Collect transcripts from real candidate sessions (with consent).
  - Analyze common mistakes and add more targeted questions.
  - Fine-tune the LLM or build a custom evaluation model using collected data.
  - Add more advanced Excel scenarios (e.g., file uploads, formula debugging).
  - Implement user authentication and persistent session storage.

## 10. Deployment Plan

### Local Development
- Run both FastAPI backend and Streamlit frontend locally as described in the setup section.

### Production Deployment
- **Backend:** Deploy FastAPI app to cloud platforms (AWS, GCP, Azure) or containerized deployment.
- **Frontend:** Deploy Streamlit app to Streamlit Cloud or similar platforms.
- **Database:** Add persistent session storage (PostgreSQL, MongoDB).
- **Secrets Management:** Use cloud platform secrets management for API keys.

## 11. Limitations & Future Work

- **No user authentication** (MVP only).
- **Session state is in-memory** and not persistent across server restarts.
- **LLM cost and latency** (depends on API provider).
- **UI is basic** (can be improved for production).
- **No database integration** for persistent storage.

### Future Enhancements
- Add user authentication and role-based access
- Implement persistent session storage with database
- Add more sophisticated Excel question types
- Create admin dashboard for interview analytics
- Add video/audio interview capabilities
- Implement A/B testing for different question sets

--- 
