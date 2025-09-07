# app.py
import streamlit as st
from utils import extract_text_from_pdf
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables (for OpenAI key if you have one)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Try import openai only if API key exists
openai = None
if OPENAI_API_KEY:
    try:
        import openai as _openai
        openai = _openai
        openai.api_key = OPENAI_API_KEY
    except Exception as e:
        openai = None
        st.warning(f"OpenAI library not available: {e}")

st.set_page_config(page_title="Smart Resume Reviewer", layout="wide")
st.title("📄 Smart Resume Reviewer")

# Resume Upload/Input
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    resume_text = extract_text_from_pdf(bytes_data)

manual_text = st.text_area("Or paste your resume text here", value="", height=200)
if manual_text.strip():
    resume_text = manual_text

job_role = st.text_input("Target job role (e.g., Data Scientist)")
job_desc = st.text_area("Optional: Job description (paste here)")

def fallback_feedback(resume_text, job_role, job_desc):
    txt = resume_text.lower()
    bullets = ("-" in resume_text) or ("\n•" in resume_text) or ("\n*" in resume_text)
    feedback = []
    if "education" in txt:
        feedback.append("• Education section found.")
    else:
        feedback.append("• Add an Education section.")
    if "experience" in txt or "company" in txt:
        feedback.append("• Experience section found.")
    else:
        feedback.append("• Add an Experience section.")
    if "skills" in txt:
        feedback.append("• Skills section found.")
    else:
        feedback.append("• Add a Skills section.")
    if not bullets:
        feedback.append("• Use bullet points for clarity.")
    words = len(resume_text.split())
    feedback.append(f"• Resume length: {words} words.")
    if job_desc:
        feedback.append("• Tailor skills/keywords from the job description.")
    return "\n".join(feedback)

if st.button("🔍 Review Resume"):
    if not resume_text.strip():
        st.error("Please upload or paste a resume first.")
    elif not job_role.strip():
        st.error("Please enter a target job role.")
    else:
        if openai is not None:
            st.info("Contacting AI to generate feedback...")
            try:
                response = openai.ChatCompletion.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert career coach."},
                        {"role": "user", "content": f"Review this resume for {job_role}. Job description: {job_desc}\nResume:\n{resume_text}"}
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                feedback = response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                feedback = f"Error calling AI: {e}\n\nUsing fallback...\n" + fallback_feedback(resume_text, job_role, job_desc)
        else:
            st.warning("No OpenAI API key found. Using fallback rules.")
            feedback = fallback_feedback(resume_text, job_role, job_desc)

        st.subheader("📊 Feedback")
        st.write(feedback)
