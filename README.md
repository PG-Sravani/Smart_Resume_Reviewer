# Smart Resume Reviewer

This is an LLM-powered application that reviews resumes and offers tailored, constructive feedback for a specific job role.  
It helps job seekers optimize their resumes to better align with job descriptions and industry expectations.

## 🚀 Features
- Upload resume (PDF format).
- Paste job description to guide the feedback.
- AI-powered feedback:
  - Missing skills or keywords.
  - Recommendations for improvement.
  - Highlight redundant/vague language.
  - Suggestions to tailor experience to the job role.

## 🛠️ Tech Stack
- **Language**: Python
- **Libraries**: Streamlit, OpenAI, pdfplumber
- **Deployment**: Streamlit Cloud

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
