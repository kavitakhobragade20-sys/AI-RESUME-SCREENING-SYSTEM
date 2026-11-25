from flask import Flask, render_template_string, request
import PyPDF2
import re

app = Flask(name)

JOBS = {
"Python Developer": ["Python", "Flask", "SQL", "Git"],
"Data Analyst": ["Python", "SQL", "Excel", "Power BI"],
"Frontend Developer": ["HTML", "CSS", "JavaScript", "React"],
"Backend Developer": ["Python", "SQL", "Flask", "Django"],
"Machine Learning Intern": ["Python", "Machine Learning", "Data Analysis"]
}

HTML = """

<!DOCTYPE html><html>
<head>
<title>ResumeMatch AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#eef2ff;margin:0;color:#172554}
header{background:#172554;color:white;padding:25px;text-align:center}
main{max-width:750px;margin:30px auto;padding:20px}
.card{background:white;padding:25px;border-radius:14px;box-shadow:0 3px 15px #ccd}
button{background:#2563eb;color:white;padding:12px 22px;border:0;border-radius:7px}
input{margin:20px 0}
.result{padding:15px;margin:12px 0;background:#eff6ff;border-radius:8px}
</style>
</head>
<body>
<header><h1>ResumeMatch AI</h1>
<p>AI-Based Resume Screening and Job Recommendation System</p></header>
<main>
<div class="card">
<h2>Upload Your Resume</h2>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="resume" accept=".pdf,.txt" required>
<br><button type="submit">Analyze Resume</button>
</form>
{% if skills is not none %}
<h2>Detected Skills</h2>
<p>{{ skills|join(', ') if skills else 'No matching skills found' }}</p>
<h2>Job Recommendations</h2>
{% for job, score in results %}
<div class="result"><b>{{job}}</b><br>
Skill Match: {{score}}%</div>
{% endfor %}
{% endif %}
</div>
</main>
</body>
</html>
"""@app.route("/", methods=["GET", "POST"])
def home():
skills = None
results = []

if request.method == "POST":
    file = request.files.get("resume")

    if file and file.filename:
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            text = " ".join(
                page.extract_text() or "" for page in reader.pages
            )
        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")
        else:
            return "Please upload a PDF or TXT file."

        text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text).lower()

        all_skills = set(skill for job_skills in JOBS.values()
                         for skill in job_skills)

        skills = [s for s in all_skills if s.lower() in text]

        for job, required in JOBS.items():
            matched = [s for s in required if s in skills]
            score = round(len(matched) / len(required) * 100)
            results.append((job, score))

        results.sort(key=lambda x: x[1], reverse=True)

return render_template_string(HTML, skills=skills, results=results)

if name == "main":
app.run(host="0.0.0.0", port=5000)
