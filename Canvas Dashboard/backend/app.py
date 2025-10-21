from flask import Flask, jsonify
from flask_cors import CORS
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable cross-origin for React frontend

CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")
API_KEY = os.getenv("CANVAS_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Get courses with grades
@app.route("/api/courses")
def get_courses():
    url = f"{CANVAS_BASE_URL}/courses?enrollment_state=active"
    r = requests.get(url, headers=HEADERS)
    courses = r.json()

    course_data = []
    for c in courses:
        enrollments = c.get("enrollments")
        if not enrollments:
            continue
        grade = enrollments[0].get("computed_current_score")
        course_data.append({
            "id": c["id"],
            "name": c["name"],
            "grade": grade,
        })
    return jsonify(course_data)

# Calculate GPA (simple 4.0 scale)
@app.route("/api/gpa")
def calculate_gpa():
    url = f"{CANVAS_BASE_URL}/courses?enrollment_state=active"
    r = requests.get(url, headers=HEADERS)
    courses = r.json()

    total_points = 0
    total_courses = 0
    for c in courses:
        enrollments = c.get("enrollments")
        if not enrollments:
            continue
        grade = enrollments[0].get("computed_current_score")
        if grade is None:
            continue

        if grade >= 90: gpa = 4.0
        elif grade >= 80: gpa = 3.0
        elif grade >= 70: gpa = 2.0
        elif grade >= 60: gpa = 1.0
        else: gpa = 0.0

        total_points += gpa
        total_courses += 1

    gpa = round(total_points / total_courses, 2) if total_courses > 0 else "N/A"
    return jsonify({"gpa": gpa})

# Upcoming assignments (next 7 days)
@app.route("/api/upcoming")
def upcoming_assignments():
    url_courses = f"{CANVAS_BASE_URL}/courses?enrollment_state=active"
    r_courses = requests.get(url_courses, headers=HEADERS)
    courses = r_courses.json()

    upcoming = []
    for c in courses:
        course_id = c["id"]
        url_assignments = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments"
        r_assignments = requests.get(url_assignments, headers=HEADERS)
        assignments = r_assignments.json()
        for a in assignments:
            upcoming.append({
                "course": c["name"],
                "name": a["name"],
                "due_at": a.get("due_at"),
                "points_possible": a.get("points_possible")
            })
    return jsonify(upcoming)

if __name__ == "__main__":
    app.run(debug=True)
