from resume_parser import extract_resume_text
from job_matcher import calculate_similarity

#Loading the Resume
resume_text = extract_resume_text("Ace24.pdf")

#sample job description
job_description = """We are looking for a software engineer skilled in Python, machine learning, and data analysis.
The candidate must be able to work in a fast-paced environment and collaborate with cross-functional teams.
"""

#To calculate the match:
score = calculate_similarity(resume_text, job_description)

print(f"Resume match score: {score}%")