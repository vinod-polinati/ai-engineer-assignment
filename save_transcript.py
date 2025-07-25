import os
from datetime import datetime

def save_chat_transcript(session_id, warmup_log, interview_log, final_summary):
    os.makedirs("transcripts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"transcripts/{session_id}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🧠 Excel Mock Interview Transcript\n")
        f.write(f"Session ID: {session_id}\n")
        f.write(f"Date: {timestamp}\n\n")

        f.write("=== Warm-up ===\n")
        for i, qa in enumerate(warmup_log):
            f.write(f"Q{i+1}: {qa['question']}\n")
            f.write(f"A{i+1}: {qa['answer']}\n\n")

        f.write("=== Technical Interview ===\n")
        for i, qa in enumerate(interview_log):
            f.write(f"Q{i+1}: {qa['question']}\n")
            f.write(f"A{i+1}: {qa['answer']}\n")
            f.write(f"Evaluation: {qa['evaluation']}\n\n")

        f.write("=== Final Feedback ===\n")
        f.write(final_summary + "\n")

    return filename
