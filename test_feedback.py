
from resume_parser import extract_resume_text
from feedback_generator import generate_feedback

# Load resume
resume_text = extract_resume_text("Ace24.pdf")

# Sample job description
job_description = """
Looking for a Python developer with experience in machine learning, data analysis, and API integration.
The ideal candidate is also comfortable with Git, Agile, and team collaboration.
"""

# Generate feedback
feedback = generate_feedback(resume_text, job_description)
print(feedback)
