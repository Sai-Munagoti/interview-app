import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, render_template_string
import mysql.connector
import random
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa

# FIXED IMPORTS (backend. removed)
from questions import questions
from devops_questions import devops_questions

# Correct template/static directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "static"))

# Flask app initialization
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "exam-secret-key"


# -------------------------------------------
# Database connection
# -------------------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpass"),
        database=os.getenv("MYSQL_DATABASE", "devops_exam")
    )


# -------------------------------------------
# Routes
# -------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/devops")
def devops_page():
    return render_template("devops.html", devops_questions=devops_questions)


@app.route("/start", methods=["POST"])
def start_exam():
    session["name"] = request.form["name"]
    session["gender"] = request.form["gender"]
    session["email"] = request.form["email"]

    # Select 15 random questions
    selected = random.sample(questions, 15)

    # Add index so HTML can map answers
    for i, q in enumerate(selected):
        q["index"] = i

    session["questions"] = selected

    return render_template(
        "exam.html",
        name=session["name"],
        gender=session["gender"],
        email=session["email"],
        questions=selected
    )


@app.route("/submit", methods=["POST"])
def submit_exam():
    questions_session = session.get("questions", [])

    score = 0
    for q in questions_session:
        idx = q["index"]
        ans = request.form.get(f"question_{idx}")
        if ans == q["answer"]:
            score += 1

    # Store results into MySQL
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO results (username, gender, email, score) VALUES (%s, %s, %s, %s)",
        (session["name"], session["gender"], session["email"], score)
    )

    db.commit()
    cursor.close()
    db.close()

    session["exam_score"] = score

    return render_template("result.html", score=score)


@app.route("/admin")
def admin_view():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT username, gender, email, score FROM results ORDER BY id DESC")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin.html", records=data)


# -------------------------------------------
# Certificate Generation
# -------------------------------------------
def read_certificate_template():
    path = os.path.join(BASE_DIR, "certificate.html")
    if not os.path.exists(path):
        return """
        <h1>Certificate</h1>
        <p>{{ name }}</p>
        <p>{{ score }}</p>
        """
    return open(path).read()


@app.route("/download_certificate")
def download_certificate():
    template = read_certificate_template()

    html = render_template_string(
        template,
        name=session.get("name"),
        score=session.get("exam_score"),
        date=datetime.now().strftime("%B %d, %Y")
    )

    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)

    response = make_response(pdf.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=certificate.pdf"

    return response


# -------------------------------------------
# Run Application
# -------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
