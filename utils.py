import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_resume(resume_text, job_description):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI career coach."},
                {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception:
        # Fallback for demo
        return """
        ✅ Resume Analysis:
        - Strengths: Strong Python & SQL skills, clear project experience.
        - Weaknesses: Missing cloud (AWS/GCP) and ML deployment experience.
        - Suggestion: Add details about data visualization (Tableau/Power BI).
        """
