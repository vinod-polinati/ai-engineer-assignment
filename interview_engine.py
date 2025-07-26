from llm_service import ask_llm, evaluate_answer, generate_feedback
from prompts import INTERVIEW_QUESTIONS
from save_transcript import save_chat_transcript  # added
import traceback

FILLER_ANSWERS = [
    "okay", "ok", "i get it", "yeah i get it", "got it", "makes sense",
    "understood", "cool", "alright", "sure", "thanks", "thank you"
]

CONFUSION_KEYWORDS = [
    "don't understand", "didn't understand", "can you explain",
    "not sure", "what does", "elaborate", "please clarify", "confused"
]

WARMUP_QUESTIONS = [
    "Can you briefly introduce yourself?",
    "How comfortable are you with using Excel on a daily basis?",
    "What kinds of Excel tasks do you typically perform?"
]

class InterviewEngine:
    def __init__(self):
        self.sessions = {}

    async def handle_message(self, session_id, message):
        try:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "stage": "intro",
                    "current_q": 0,
                    "warmup_q": 0,
                    "answers": [],
                    "warmup_log": [],
                    "is_clarifying": False
                }

            session = self.sessions[session_id]
            user_message = message.strip().lower()

            # Step 1: Intro
            if session["stage"] == "intro":
                session["stage"] = "warmup"
                return (
                    "Hi! I'm your AI Excel interviewer. Before we begin, "
                    "let's get to know each other a bit.\n\n" +
                    WARMUP_QUESTIONS[0]
                )

            # Step 2: Warmup
            elif session["stage"] == "warmup":
                session["warmup_log"].append({
                    "question": WARMUP_QUESTIONS[session["warmup_q"]],
                    "answer": message
                })
                session["warmup_q"] += 1
                if session["warmup_q"] < len(WARMUP_QUESTIONS):
                    return WARMUP_QUESTIONS[session["warmup_q"]]
                else:
                    session["stage"] = "interview"
                    return f"Thanks for sharing! Let's begin the interview.\n\n{INTERVIEW_QUESTIONS[0]}"

            # Step 3: Interview
            elif session["stage"] == "interview":
                current_q = session["current_q"]

                if session.get("is_clarifying", False):
                    if user_message in FILLER_ANSWERS:
                        return "Great! Now could you try answering the question in your own words?"
                    session["is_clarifying"] = False
                    try:
                        eval = await evaluate_answer(INTERVIEW_QUESTIONS[current_q], message)
                        session["answers"].append({
                            "question": INTERVIEW_QUESTIONS[current_q],
                            "answer": message,
                            "evaluation": eval
                        })
                    except Exception as e:
                        print(f"Error evaluating answer: {e}")
                        session["answers"].append({
                            "question": INTERVIEW_QUESTIONS[current_q],
                            "answer": message,
                            "evaluation": "Error evaluating answer"
                        })
                    
                    session["current_q"] += 1
                    if session["current_q"] >= len(INTERVIEW_QUESTIONS):
                        session["stage"] = "summary"
                        try:
                            summary = await generate_feedback(session["answers"])
                        except Exception as e:
                            print(f"Error generating feedback: {e}")
                            summary = "Error generating feedback. Interview completed."
                        
                        # Try to save transcript but don't let it block the response
                        try:
                            save_chat_transcript(
                                session_id=session_id,
                                warmup_log=session.get("warmup_log", []),
                                interview_log=session["answers"],
                                final_summary=summary
                            )
                        except Exception as e:
                            print(f"PDF generation failed (non-critical): {e}")
                            print(f"Traceback: {traceback.format_exc()}")
                        return summary
                    else:
                        return INTERVIEW_QUESTIONS[session["current_q"]]

                if any(keyword in user_message for keyword in CONFUSION_KEYWORDS):
                    session["is_clarifying"] = True
                    try:
                        explanation = await ask_llm(
                            f"""You are an Excel interviewer.\nA candidate is confused by this question: \"{INTERVIEW_QUESTIONS[current_q]}\"\nGive a short clarification or rephrasing -- do not give the full answer.\n"""
                        )
                        return f"Sure! Here's a hint:\n\n{explanation}"
                    except Exception as e:
                        print(f"Error generating clarification: {e}")
                        return f"Let me rephrase the question: {INTERVIEW_QUESTIONS[current_q]}"

                # Normal evaluation
                try:
                    eval = await evaluate_answer(INTERVIEW_QUESTIONS[current_q], message)
                    session["answers"].append({
                        "question": INTERVIEW_QUESTIONS[current_q],
                        "answer": message,
                        "evaluation": eval
                    })
                except Exception as e:
                    print(f"Error evaluating answer: {e}")
                    session["answers"].append({
                        "question": INTERVIEW_QUESTIONS[current_q],
                        "answer": message,
                        "evaluation": "Error evaluating answer"
                    })
                
                session["current_q"] += 1
                if session["current_q"] >= len(INTERVIEW_QUESTIONS):
                    session["stage"] = "summary"
                    try:
                        summary = await generate_feedback(session["answers"])
                    except Exception as e:
                        print(f"Error generating feedback: {e}")
                        summary = "Error generating feedback. Interview completed."
                    
                    # Try to save transcript but don't let it block the response
                    try:
                        save_chat_transcript(
                            session_id=session_id,
                            warmup_log=session.get("warmup_log", []),
                            interview_log=session["answers"],
                            final_summary=summary
                        )
                    except Exception as e:
                        print(f"PDF generation failed (non-critical): {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                    return summary
                else:
                    return INTERVIEW_QUESTIONS[session["current_q"]]

            # Step 4: Done
            elif session["stage"] == "summary":
                return "Interview completed. Click restart to begin again."

            return "Unexpected error. Please refresh."
            
        except Exception as e:
            print(f"Critical error in handle_message: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return "An unexpected error occurred. Please try again."
