import streamlit as st
import uuid
import httpx
import os
from datetime import datetime

# --- INTERVIEW QUESTIONS ---
INTERVIEW_QUESTIONS = [
    "How would you use a VLOOKUP function in Excel?",
    "Explain the difference between absolute and relative cell references.",
    "How do pivot tables help in data analysis?",
    "Can you describe how to use conditional formatting effectively?",
    "What’s the purpose of using named ranges in Excel?"
]

WARMUP_QUESTIONS = [
    "Can you briefly introduce yourself?",
    "How comfortable are you with using Excel on a daily basis?",
    "What kinds of Excel tasks do you typically perform?"
]

FILLER_ANSWERS = [
    "okay", "ok", "i get it", "yeah i get it", "got it", "makes sense",
    "understood", "cool", "alright", "sure", "thanks", "thank you"
]

CONFUSION_KEYWORDS = [
    "don't understand", "didn't understand", "can you explain",
    "not sure", "what does", "elaborate", "please clarify", "confused"
]

# --- LLM Service (Groq API) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3-70b-8192")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def ask_llm(prompt: str):
    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    with httpx.Client() as client:
        response = client.post(GROQ_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()

def evaluate_answer(question, answer):
    prompt = f"""
You are an expert Excel interviewer. Evaluate the following candidate answer.\n\nQuestion: "{question}"\nAnswer: "{answer}"\n\nGive a score out of 10, and briefly explain the rating.
"""
    return ask_llm(prompt)

def generate_feedback(answer_log):
    qas = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\nEval: {qa['evaluation']}" for qa in answer_log])
    prompt = f"""
Here is an Excel mock interview session:\n\n{qas}\n\nSummarize the candidate’s performance: strengths, weaknesses, and overall impression.
"""
    return ask_llm(prompt)

def format_transcript(session_id, warmup_log, interview_log, final_summary):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    lines = [
        "🧠 Excel Mock Interview Transcript",
        f"Session ID: {session_id}",
        f"Date: {timestamp}",
        "",
        "=== Warm-up ==="
    ]
    for i, qa in enumerate(warmup_log):
        lines.append(f"Q{i+1}: {qa['question']}")
        lines.append(f"A{i+1}: {qa['answer']}")
        lines.append("")
    lines.append("=== Technical Interview ===")
    for i, qa in enumerate(interview_log):
        lines.append(f"Q{i+1}: {qa['question']}")
        lines.append(f"A{i+1}: {qa['answer']}")
        lines.append(f"Evaluation: {qa['evaluation']}")
        lines.append("")
    lines.append("=== Final Feedback ===")
    lines.append(final_summary)
    return "\n".join(lines)

# --- Streamlit UI ---
st.set_page_config(page_title="Excel AI Interviewer", page_icon="🧠", layout="centered")
st.title("🧠 Excel Mock Interview")

# --- Session State Initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "warmup_q" not in st.session_state:
    st.session_state.warmup_q = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "warmup_log" not in st.session_state:
    st.session_state.warmup_log = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "is_clarifying" not in st.session_state:
    st.session_state.is_clarifying = False
if "summary" not in st.session_state:
    st.session_state.summary = None
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "sender": "bot",
        "text": "Hi, I'm your AI Excel interviewer. Type anything to begin."
    }]

# --- Restart Button ---
if st.button("🔄 Restart Interview"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.stage = "intro"
    st.session_state.warmup_q = 0
    st.session_state.current_q = 0
    st.session_state.warmup_log = []
    st.session_state.answers = []
    st.session_state.is_clarifying = False
    st.session_state.summary = None
    st.session_state.messages = [{
        "sender": "bot",
        "text": "Hi, I'm your AI Excel interviewer. Type anything to begin."
    }]
    st.rerun()

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["sender"] == "user" else "assistant"):
        st.markdown(msg["text"])

# --- Chat Input Handler ---
prompt = st.chat_input("Type your response here...")
if prompt and st.session_state.stage != "summary":
    st.session_state.messages.append({"sender": "user", "text": prompt})
    user_message = prompt.strip().lower()

    # --- Interview Logic ---
    if st.session_state.stage == "intro":
        with st.spinner("Starting interview..."):
            st.session_state.stage = "warmup"
            bot_reply = (
                "Hi! I'm your AI Excel interviewer. Before we begin, "
                "let's get to know each other a bit.\n\n" + WARMUP_QUESTIONS[0]
            )
        st.session_state.messages.append({"sender": "bot", "text": bot_reply})

    elif st.session_state.stage == "warmup":
        st.session_state.warmup_log.append({
            "question": WARMUP_QUESTIONS[st.session_state.warmup_q],
            "answer": prompt
        })
        st.session_state.warmup_q += 1
        if st.session_state.warmup_q < len(WARMUP_QUESTIONS):
            bot_reply = WARMUP_QUESTIONS[st.session_state.warmup_q]
        else:
            with st.spinner("Starting technical interview..."):
                st.session_state.stage = "interview"
                bot_reply = "Thanks for sharing! Let's begin the interview.\n\n" + INTERVIEW_QUESTIONS[0]
        st.session_state.messages.append({"sender": "bot", "text": bot_reply})

    elif st.session_state.stage == "interview":
        current_q = st.session_state.current_q
        if st.session_state.is_clarifying:
            if user_message in FILLER_ANSWERS:
                bot_reply = "Great! Now could you try answering the question in your own words?"
            else:
                st.session_state.is_clarifying = False
                with st.spinner("Evaluating your answer..."):
                    eval = evaluate_answer(INTERVIEW_QUESTIONS[current_q], prompt)
                st.session_state.answers.append({
                    "question": INTERVIEW_QUESTIONS[current_q],
                    "answer": prompt,
                    "evaluation": eval
                })
                st.session_state.current_q += 1
                if st.session_state.current_q >= len(INTERVIEW_QUESTIONS):
                    st.session_state.stage = "summary"
                    with st.spinner("Generating feedback summary..."):
                        summary = generate_feedback(st.session_state.answers)
                    st.session_state.summary = summary
                    bot_reply = summary
                else:
                    bot_reply = INTERVIEW_QUESTIONS[st.session_state.current_q]
            st.session_state.messages.append({"sender": "bot", "text": bot_reply})

        elif any(keyword in user_message for keyword in CONFUSION_KEYWORDS):
            st.session_state.is_clarifying = True
            with st.spinner("Let me clarify that question..."):
                explanation = ask_llm(
                    f"You're an Excel interviewer.\nA candidate is confused by this question: "
                    f"{INTERVIEW_QUESTIONS[current_q]}"\
                    "\nGive a short clarification or rephrasing — do not give the full answer."
                )
            bot_reply = f"Sure! Here's a hint:\n\n{explanation}"
            st.session_state.messages.append({"sender": "bot", "text": bot_reply})

        else:
            with st.spinner("Evaluating your answer..."):
                eval = evaluate_answer(INTERVIEW_QUESTIONS[current_q], prompt)
            st.session_state.answers.append({
                "question": INTERVIEW_QUESTIONS[current_q],
                "answer": prompt,
                "evaluation": eval
            })
            st.session_state.current_q += 1
            if st.session_state.current_q >= len(INTERVIEW_QUESTIONS):
                st.session_state.stage = "summary"
                with st.spinner("Generating feedback summary..."):
                    summary = generate_feedback(st.session_state.answers)
                st.session_state.summary = summary
                bot_reply = summary
            else:
                bot_reply = INTERVIEW_QUESTIONS[st.session_state.current_q]
            st.session_state.messages.append({"sender": "bot", "text": bot_reply})

# --- Transcript Download Button ---
if st.session_state.stage == "summary" and st.session_state.summary:
    transcript = format_transcript(
        st.session_state.session_id,
        st.session_state.warmup_log,
        st.session_state.answers,
        st.session_state.summary
    )
    st.download_button(
        label="📄 Download Interview Transcript",
        data=transcript,
        file_name=f"excel_mock_interview_{st.session_state.session_id}.txt",
        mime="text/plain"
    )
