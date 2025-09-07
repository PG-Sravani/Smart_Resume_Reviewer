import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import extract_text_from_pdf
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional: load API key (not used here because we use mock)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Streamlit page config
st.set_page_config(page_title="Smart Resume Reviewer", layout="wide")
st.title("📄 Smart Resume Reviewer")

# Upload PDF resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    resume_text = extract_text_from_pdf(bytes_data)

# Manual resume input
manual_text = st.text_area("Or paste your resume text here", value="", height=200)
if manual_text.strip():
    resume_text = manual_text

# Job inputs
job_role = st.text_input("Target job role (e.g., Data Scientist)")
job_desc = st.text_area("Optional: Job description (paste here)")

# 🔁 Mock feedback generator based on resume content
def generate_mock_feedback(resume_text, job_role, job_desc):
    txt = resume_text.lower()
    feedback = []

    # Simple rule-based checks
    if "python" in txt:
        feedback.append("• Good to see Python skills mentioned.")
    else:
        feedback.append("• Consider adding Python skills if relevant.")

    if "project" in txt:
        feedback.append("• Projects section helps demonstrate applied skills.")
    else:
        feedback.append("• Include at least one project to showcase your work.")

    if "intern" in txt or "internship" in txt:
        feedback.append("• Internship experience adds great value.")
    else:
        feedback.append("• Try adding relevant internships if any.")

    if "machine learning" in txt:
        feedback.append("• Machine Learning experience is a strong asset.")
    else:
        feedback.append("• If applicable, highlight any ML experience.")

    if len(txt.split()) < 300:
        feedback.append("• Resume seems a bit short. Consider expanding with more details.")
    else:
        feedback.append("• Resume length looks good.")

    if job_desc:
        feedback.append("• Make sure to align your resume with the job description.")

    # Final recommendation
    feedback.append(f"• Tailored feedback for the '{job_role}' role provided.")

    return "\n".join(feedback)

# 🟩 Button to trigger feedback
if st.button("🔍 Review Resume"):
    if not resume_text.strip():
        st.error("Please upload or paste a resume first.")
    elif not job_role.strip():
        st.error("Please enter a target job role.")
    else:
        feedback = generate_mock_feedback(resume_text, job_role, job_desc)

        st.subheader("📊 Feedback")
        st.write(feedback)
