import os
import openai
from io import BytesIO
import PyPDF2

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------- PDF Extraction --------
def extract_text_from_pdf(file_bytes):
    """
    Extract text from uploaded PDF file (bytes).
    """
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text


# -------- Resume Analysis with OpenAI --------
def analyze_resume(resume_text, job_description=""):
    """
    Send resume + job description to OpenAI for analysis.
    Falls back to mock feedback if API fails.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI career coach."},
                {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
            ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception:
        # Fallback for demo
        return """✅ Resume Analysis:
- Strengths: Strong Python & SQL skills, clear project experience.
- Weaknesses: Missing cloud (AWS/GCP) and ML deployment experience.
- Suggestion: Add details about data visualization (Tableau/Power BI)."""
