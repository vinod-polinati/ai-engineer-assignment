# AI-Powered Excel Mock Interviewer  
**Design Document**

## 1. Problem Statement

Manual Excel interviews are a bottleneck in our hiring process, causing delays and inconsistent candidate evaluations. We need an automated, scalable, and fair way to assess Excel skills for Finance, Operations, and Data Analytics roles.

## 2. Solution Overview

I built an AI-powered web app that simulates a real Excel interview. The system asks warm-up and technical questions, evaluates answers using a large language model (LLM), and provides a detailed feedback report. The goal is to save time for senior analysts and ensure consistent, unbiased candidate assessment.

## 3. System Architecture

```mermaid
flowchart TD
    A[User (Candidate)] -- Chat UI --> B[Streamlit App (frontend.py)]
    B -- LLM API Calls --> C[Groq API]
    B -- Save Transcript --> D[Downloadable Transcript]
```

- **Streamlit App:** All interview logic, LLM calls, state management, and transcript generation are handled in a single file (`frontend.py`).
- **LLM Service:** The app calls the Groq API directly for answer evaluation, clarification, and feedback.
- **Transcript:** At the end of the interview, the user can download their transcript as a text file.

## 4. Interview Flow

1. **Introduction:** The bot introduces itself and explains the process.
2. **Warm-up:** Asks 2–3 general questions to get the candidate comfortable.
3. **Technical Questions:** Asks a series of Excel-related questions.
4. **Clarification:** If the candidate is confused, the bot provides hints (not answers).
5. **Evaluation:** Each answer is scored and explained by the LLM.
6. **Summary:** At the end, the bot gives a feedback report (strengths, weaknesses, overall impression).
7. **Transcript:** The full interview is available for download.

## 5. Technology Stack & Justification

- **Streamlit:**  
  *All logic is in a single Streamlit app (`frontend.py`), making it easy to deploy and maintain. Streamlit provides a user-friendly chat interface and session management.*
- **LLM Provider:** Groq API (Llama-3)  
  *Provides high-quality language understanding and generation for answer evaluation and feedback. The API key is managed securely using Streamlit Cloud secrets.*
- **Transcript Storage:** Downloadable file  
  *Users can download their interview transcript at the end of the session.*

## 6. Key Features

- **Conversational AI:** Simulates a real interview with multi-turn dialogue.
- **Dynamic Evaluation:** Uses LLM to score and explain answers.
- **Clarification:** Detects confusion and provides hints.
- **Session Management:** Each interview is tracked by a unique session ID.
- **Feedback Report:** Summarizes candidate performance at the end.
- **Transcript Download:** Users can download their full interview log for transparency.

## 7. Cold Start & Improvement Plan

- **Cold Start:**  
  The system does not require any pre-existing dataset. It uses LLMs, which are already trained on general Excel knowledge.
- **Improvement Plan:**  
  - Collect transcripts from real candidate sessions (with consent).
  - Analyze common mistakes and add more targeted questions.
  - Fine-tune the LLM or build a custom evaluation model using collected data.
  - Add more advanced Excel scenarios (e.g., file uploads, formula debugging).

## 8. Deployment Plan

- **Streamlit Cloud:** The app is deployed on Streamlit Cloud. All logic is in `frontend.py`.
- **Secrets Management:** The Groq API key is securely managed using Streamlit Cloud's secrets feature.
- **How to Deploy:**
  1. Push the code to GitHub.
  2. Connect the repo to Streamlit Cloud and set the main file to `frontend.py`.
  3. Add the `GROQ_API_KEY` in the app's secrets settings.
  4. Deploy and share the public link.

## 9. Limitations & Future Work

- **No user authentication** (MVP only).
- **Session state is in-memory (per user session)** and not persistent across server restarts.
- **LLM cost and latency** (depends on API provider).
- **UI is basic** (can be improved for production).

--- 
