# test_parser.py

from resume_parser import extract_resume_text

file_path = "Ace24.pdf"  
text = extract_resume_text(file_path)
print(text)
