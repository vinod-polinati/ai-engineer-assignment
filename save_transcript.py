import os
from datetime import datetime
from fpdf import FPDF

def sanitize_text(text):
    # Replace curly quotes/apostrophes and other common non-ASCII chars
    replacements = {
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"',
        '–': '-',
        '—': '-',
        '…': '...',
        '•': '-',
        '→': '->',
        '←': '<-',
        'é': 'e',
        'á': 'a',
        'ö': 'o',
        # Add more as needed
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Remove any other non-latin1 characters
    return text.encode('latin-1', 'ignore').decode('latin-1')

def save_chat_transcript(session_id, warmup_log, interview_log, final_summary):
    os.makedirs("transcripts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"transcripts/{session_id}_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, sanitize_text("Excel Mock Interview Transcript"), ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, sanitize_text(f"Session ID: {session_id}"), ln=True)
    pdf.cell(0, 10, sanitize_text(f"Date: {timestamp}"), ln=True)
    pdf.ln(5)

    # Warm-up Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, sanitize_text("=== Warm-up ==="), ln=True)
    pdf.set_font("Arial", '', 12)
    for i, qa in enumerate(warmup_log):
        pdf.multi_cell(0, 8, sanitize_text(f"Q{i+1}: {qa['question']}"))
        pdf.multi_cell(0, 8, sanitize_text(f"A{i+1}: {qa['answer']}"))
        pdf.ln(2)

    # Technical Interview Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, sanitize_text("=== Technical Interview ==="), ln=True)
    pdf.set_font("Arial", '', 12)
    for i, qa in enumerate(interview_log):
        pdf.multi_cell(0, 8, sanitize_text(f"Q{i+1}: {qa['question']}"))
        pdf.multi_cell(0, 8, sanitize_text(f"A{i+1}: {qa['answer']}"))
        pdf.multi_cell(0, 8, sanitize_text(f"Evaluation: {qa['evaluation']}"))
        pdf.ln(2)

    # Final Feedback Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, sanitize_text("=== Final Feedback ==="), ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, sanitize_text(final_summary))

    pdf.output(filename)
    return filename