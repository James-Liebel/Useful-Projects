# app.py
from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

CANVAS_API_URL = os.getenv("CANVAS_API_URL")  # e.g. https://your-school.instructure.com/api/v1
CANVAS_API_KEY = os.getenv("CANVAS_API_KEY")
HEADERS = {"Authorization": f"Bearer {CANVAS_API_KEY}"}

# Fetch all courses for the user
def get_courses():
    r = requests.get(f"{CANVAS_API_URL}/courses", headers=HEADERS)
    if r.status_code != 200:
        return []
    return r.json()

# Fetch assignments for a specific course
def get_assignments(course_id):
    r = requests.get(f"{CANVAS_API_URL}/courses/{course_id}/assignments", headers=HEADERS)
    if r.status_code != 200:
        return []
    return r.json()

# Filter assignments due in the next 7 days
def filter_upcoming_assignments(assignments):
    now = datetime.now()
    upcoming = []
    for a in assignments:
        if a.get("due_at"):
            due_date = datetime.fromisoformat(a["due_at"].replace("Z", "+00:00"))
            if now <= due_date <= now + timedelta(days=7):
                upcoming.append({
                    "name": a["name"],
                    "course_id": a["course_id"],
                    "due_at": a["due_at"]
                })
    return upcoming

# Calculate GPA (dummy example: real logic depends on Canvas data)
def calculate_gpa(courses, quarter="All"):
    grades = []
    for c in courses:
        if quarter != "All" and c.get("enrollment_term_name") != quarter:
            continue
        grade = c.get("enrollment_term_grade")
        if grade:
            try:
                grades.append(float(grade))
            except:
                pass
    return round(sum(grades) / len(grades), 2) if grades else None

# Get all terms/quarters
def get_quarters():
    r = requests.get(f"{CANVAS_API_URL}/accounts/1/terms", headers=HEADERS)
    if r.status_code != 200:
        return ["All"]
    terms = r.json()
    quarters = ["All"]
    for t in terms:
        quarters.append(t.get("name"))
    return quarters

@app.route("/courses")
def courses_endpoint():
    quarter = request.args.get("quarter", "All")
    courses = get_courses()
    gpa = calculate_gpa(courses, quarter)
    courses_data = []
    all_assignments = []

    for c in courses:
        if quarter != "All" and c.get("enrollment_term_name") != quarter:
            continue

        assignments = get_assignments(c["id"])
        upcoming = filter_upcoming_assignments(assignments)
        all_assignments.extend(upcoming)

        courses_data.append({
            "id": c["id"],
            "name": c.get("name"),
            "grade": c.get("enrollment_term_grade"),
        })

    quarters = get_quarters()

    return jsonify({
        "gpa": gpa,
        "courses": courses_data,
        "upcoming_assignments": all_assignments,
        "quarters": quarters
    })

if __name__ == "__main__":
    app.run(debug=True)
