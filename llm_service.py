import os
import httpx
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def ask_llm(prompt: str):
    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()

async def evaluate_answer(question, answer):
    prompt = f"""
You are an expert Excel interviewer. Evaluate the following candidate answer.

Question: "{question}"
Answer: "{answer}"

Give a score out of 10, and briefly explain the rating.
"""
    return await ask_llm(prompt)

async def generate_feedback(answer_log):
    qas = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\nEval: {qa['evaluation']}" for qa in answer_log])
    prompt = f"""
Here is an Excel mock interview session:

{qas}

Summarize the candidate’s performance: strengths, weaknesses, and overall impression.
"""
    return await ask_llm(prompt)
