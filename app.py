# app.py

from flask import Flask, request, render_template, send_file, session, jsonify
import os
import io
from resume_parser import extract_resume_text
from job_matcher import calculate_similarity, calculate_similarity_bert
from feedback_generator import generate_feedback
from ai_suggester import get_resume_suggestions
from openai import OpenAI

# === Flask App Setup ===
app = Flask(__name__)
app.secret_key = 'your-super-secret-key'  # Needed for session memory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Global Feedback for Download ===
global_feedback = ""

# === Home Page ===
@app.route('/', methods=['GET', 'POST'])
def index():
    global global_feedback
    score = None
    feedback = ""
    suggestions = ""

    if request.method == 'POST':
        file = request.files['resume']
        job_description = request.form['job_description']

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            resume_text = extract_resume_text(file_path)
            use_bert = 'use_bert' in request.form

            # Matching method
            score = calculate_similarity_bert(resume_text, job_description) if use_bert else calculate_similarity(resume_text, job_description)
            feedback = generate_feedback(resume_text, job_description)
            global_feedback = feedback
            suggestions = get_resume_suggestions(resume_text, job_description)

            # Start chat memory
            session['chat_history'] = [
                {"role": "system", "content": "You are a helpful resume improvement assistant."},
                {"role": "user", "content": f"My resume: {resume_text[:1000]}..."},
                {"role": "user", "content": f"Job description: {job_description[:1000]}..."},
                {"role": "assistant", "content": suggestions}
            ]

    return render_template('index.html', score=score, feedback=feedback, suggestions=suggestions)

# === Feedback Download ===
@app.route('/download-feedback')
def download_feedback():
    global global_feedback
    plain_feedback = global_feedback.replace('<br>', '\n').replace('<li>', '- ').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
    file = io.BytesIO(plain_feedback.encode('utf-8'))
    return send_file(file, mimetype='text/plain', as_attachment=True, download_name='feedback.txt')

# === Chat Endpoint with Memory + Logging ===
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"reply": "⚠️ Missing OpenAI API key."})

    client = OpenAI(api_key=api_key)
    chat_history = session.get('chat_history', [])
    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-3.5-turbo if preferred
            messages=chat_history,
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": ai_reply})
        session['chat_history'] = chat_history

        # Save to file
        with open("chat_logs.txt", "a", encoding="utf-8") as f:
            f.write(f"User: {user_message}\nAI: {ai_reply}\n\n")

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

# === Start App ===
if __name__ == '__main__':
    app.run(debug=True)
