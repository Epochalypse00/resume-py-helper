from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

def calculate_similarity_bert(resume_text, job_description_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([resume_text, job_description_text])
    resume_vec, job_vec = embeddings[0], embeddings[1]

    cosine_sim = np.dot(resume_vec, job_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(job_vec))

def calculate_similarity(resume_text, job_description_text):
   
    documents = [resume_text, job_description_text]

    vectorizer = TfidfVectorizer(stop_words='english') #converts text into numerical data
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] #How close the resume is to the job description

    return round(similarity_score * 100, 2) #returning as percentage like 67.55%