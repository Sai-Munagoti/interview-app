# backend/app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, make_response, render_template_string, jsonify
import random
import mysql.connector
from io import BytesIO
from datetime import datetime
from xhtml2pdf import pisa

# Ensure we can import questions and devops_questions which live in the same folder
from questions import questions
from devops_questions import devops_questions

# Build absolute paths for folders (this app.py lives in backend/)
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))  # ../frontend relative to backend/
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))     # optional, adjust if you have static/

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,   # use frontend/ as templates
    static_folder=STATIC_DIR        # optional static folder (if you use one)
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'devops-exam-secret-key')


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'rootpass'),
        database=os.getenv('MYSQL_DATABASE', 'devops_exam')
    )


def read_certificate_template():
    path = os.path.join(BASE_DIR, 'certificate.html')
    if not os.path.exists(path):
        # Safe fallback: return a minimal in-memory template if certificate.html missing
        return """<html><body><h1>Certificate</h1><p>Name: {{ name }}</p><p>Score: {{ score }}</p><p>Date: {{ date }}</p></body></html>"""
    with open(path, 'r') as file:
        return file.read()


@app.route('/')
def index():
    # This will render frontend/index.html
    return render_template('index.html')


# New route: DevOps Q&A page (renders devops.html from frontend/)
@app.route('/devops')
def devops_page():
    return render_template('devops.html', devops_questions=devops_questions)


# Optional API endpoint that returns JSON
@app.route('/devops/api')
def devops_api():
    return jsonify(devops_questions)


@app.route('/start', methods=['POST'])
def start_exam():
    # Use .get to avoid KeyError if a field missing
    session['name'] = request.form.get('name', '')
    session['gender'] = request.form.get('gender', '')
    session['email'] = request.form.get('email', '')

    # ensure there are enough questions
    try:
        sample_count = 15
        if len(questions) < sample_count:
            sample_count = len(questions)
        selected_questions = random.sample(questions, sample_count)
    except Exception:
        # fallback to full list if something goes wrong with sampling
        selected_questions = questions.copy()

    for i, q in enumerate(selected_questions):
        q['index'] = i
    session['questions'] = selected_questions

    return render_template('exam.html',
                           name=session.get('name'),
                           gender=session.get('gender'),
                           email=session.get('email'),
                           questions=selected_questions)


@app.route('/submit', methods=['POST'])
def submit_exam():
    try:
        questions_in_session = session.get('questions', [])
        for i in range(len(questions_in_session)):
            if f'question_{i}' not in request.form:
                return "Please answer all questions", 400

        db = get_db_connection()
        cursor = db.cursor()

        score = 0
        for i, q in enumerate(session['questions']):
            user_answer = request.form.get(f'question_{i}')
            if user_answer is not None and user_answer == q.get('answer'):
                score += 1

        cursor.execute(
            "INSERT INTO results (username, gender, email, score) VALUES (%s, %s, %s, %s)",
            (session.get('name'), session.get('gender'), session.get('email'), score)
        )
        db.commit()

        session['exam_score'] = score

        return render_template('result.html',
                               name=session.get('name'),
                               score=score,
                               total=len(questions_in_session))
    except Exception as e:
        app.logger.exception("Database error during submit_exam")   # logs full traceback
        return "An error occurred while processing your exam", 500
    finally:
        if 'db' in locals():
            db.close()


@app.route('/download_certificate')
def download_certificate():
    try:
        name = session.get('name', 'Exam Participant')
        score = session.get('exam_score', 0)

        template = read_certificate_template()

        rendered = render_template_string(template,
                                         name=name,
                                         score=score,
                                         date=datetime.now().strftime("%B %d, %Y"))

        pdf = BytesIO()
        pisa.CreatePDF(rendered, dest=pdf)
        pdf.seek(0)

        response = make_response(pdf.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=devops_certificate_{name.replace(" ", "_")}.pdf'

        return response
    except Exception as e:
        app.logger.exception("Certificate generation error")
        return "An error occurred while generating your certificate", 500


@app.route('/admin')
def admin_view():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, gender, email, score, submitted_at FROM results")
        records = cursor.fetchall()
        return render_template('admin.html', records=records)
    except Exception as e:
        app.logger.exception("Database error on admin_view")
        return "Database error occurred", 500
    finally:
        if 'db' in locals():
            db.close()


if __name__ == '__main__':
    # When running locally from backend/ run: python app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
