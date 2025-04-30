# feedback_generator.py

import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def extract_keywords(text):
    # Simple word cleanup
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = set(words) - ENGLISH_STOP_WORDS
    return keywords

def generate_feedback(resume_text, job_description_text):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description_text)

    missing_keywords = job_keywords - resume_keywords

    if not missing_keywords:
        return "<span class='text-success'>Great! Your resume includes most of the relevant keywords from the job description.</span>"

    feedback = "<span class='text-danger'>Missing important keywords:</span><br><ul>"
    for kw in sorted(missing_keywords):
        feedback += f"<li>{kw}</li>"
    feedback += "</ul>"

    return feedback


