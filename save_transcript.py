import os
from datetime import datetime
from fpdf import FPDF

def sanitize_text(text):
    """Sanitize text to remove non-ASCII characters that cause PDF encoding errors"""
    if not text:
        return ""
    
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
    try:
        return text.encode('latin-1', 'ignore').decode('latin-1')
    except Exception:
        # Fallback: remove all non-ASCII characters
        return ''.join(char for char in text if ord(char) < 128)

def save_chat_transcript(session_id, warmup_log, interview_log, final_summary):
    """Save interview transcript as PDF with comprehensive error handling"""
    try:
        # Create transcripts directory
        os.makedirs("transcripts", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"transcripts/{session_id}_{timestamp}.pdf"

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, sanitize_text("Excel Mock Interview Transcript"), ln=True, align="C")
        pdf.ln(5)
        
        # Header info
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, sanitize_text(f"Session ID: {session_id}"), ln=True)
        pdf.cell(0, 10, sanitize_text(f"Date: {timestamp}"), ln=True)
        pdf.ln(5)

        # Warm-up Section
        if warmup_log:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, sanitize_text("=== Warm-up ==="), ln=True)
            pdf.set_font("Arial", '', 12)
            for i, qa in enumerate(warmup_log):
                try:
                    question = sanitize_text(str(qa.get('question', '')))
                    answer = sanitize_text(str(qa.get('answer', '')))
                    pdf.multi_cell(0, 8, f"Q{i+1}: {question}")
                    pdf.multi_cell(0, 8, f"A{i+1}: {answer}")
                    pdf.ln(2)
                except Exception as e:
                    print(f"Error processing warmup Q&A {i}: {e}")
                    continue

        # Technical Interview Section
        if interview_log:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, sanitize_text("=== Technical Interview ==="), ln=True)
            pdf.set_font("Arial", '', 12)
            for i, qa in enumerate(interview_log):
                try:
                    question = sanitize_text(str(qa.get('question', '')))
                    answer = sanitize_text(str(qa.get('answer', '')))
                    evaluation = sanitize_text(str(qa.get('evaluation', '')))
                    pdf.multi_cell(0, 8, f"Q{i+1}: {question}")
                    pdf.multi_cell(0, 8, f"A{i+1}: {answer}")
                    pdf.multi_cell(0, 8, f"Evaluation: {evaluation}")
                    pdf.ln(2)
                except Exception as e:
                    print(f"Error processing interview Q&A {i}: {e}")
                    continue

        # Final Feedback Section
        if final_summary:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, sanitize_text("=== Final Feedback ==="), ln=True)
            pdf.set_font("Arial", '', 12)
            try:
                pdf.multi_cell(0, 8, sanitize_text(str(final_summary)))
            except Exception as e:
                print(f"Error processing final summary: {e}")
                pdf.multi_cell(0, 8, "Final feedback could not be processed.")

        # Save the PDF
        try:
            pdf.output(filename)
            print(f"PDF transcript saved successfully: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving PDF file: {e}")
            # Fallback: save as text file
            text_filename = f"transcripts/{session_id}_{timestamp}.txt"
            try:
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(f"Excel Mock Interview Transcript\n")
                    f.write(f"Session ID: {session_id}\n")
                    f.write(f"Date: {timestamp}\n\n")
                    # Add content as text
                print(f"Text transcript saved as fallback: {text_filename}")
                return text_filename
            except Exception as e2:
                print(f"Error saving text fallback: {e2}")
                return None
                
    except Exception as e:
        print(f"Critical error in save_chat_transcript: {e}")
        return None