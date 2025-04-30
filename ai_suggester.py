import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).resolve().parent / '.env'
print("Looking for .env at:", env_path)

load_dotenv(dotenv_path=env_path)

# Load OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
print("API Key Loaded:", api_key)

# Function to get resume suggestions
def get_resume_suggestions(resume_text, job_description):
    if not api_key:
        return "❌ API key not found. Check your .env file and variable name (OPENAI_API_KEY)."

    prompt = f"""
You are a professional career assistant AI. A user has uploaded their resume and pasted a job description.

Resume:
{resume_text}

Job Description:
{job_description}

Please suggest specific improvements the user can make to their resume to better align it with the job description.
Do not rewrite the whole resume. Focus on missing areas, skill gaps, or better phrasing ideas. Keep it clear and useful.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Use "gpt-4" if you have access
        "messages": [
            {"role": "system", "content": "You are a helpful resume improvement assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"💡 AI Resume Suggestions<br>Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ AI request failed: {e}"
