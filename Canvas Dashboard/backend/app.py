# backend/app.py
from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

CANVAS_API_URL = os.getenv("CANVAS_API_URL")
API_KEY = os.getenv("CANVAS_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

@app.route("/courses")
def get_courses():
    """Return all courses from Canvas"""
    r = requests.get(f"{CANVAS_API_URL}/courses", headers=HEADERS)
    courses = r.json()
    return jsonify(courses)

@app.route("/assignments/next_week")
def get_upcoming_assignments():
    """Return assignments due in the next 7 days"""
    r = requests.get(f"{CANVAS_API_URL}/courses", headers=HEADERS)
    courses = r.json()
    upcoming = []
    now = datetime.now()
    one_week = now + timedelta(days=7)

    for course in courses:
        course_id = course['id']
        ar = requests.get(f"{CANVAS_API_URL}/courses/{course_id}/assignments", headers=HEADERS)
        assignments = ar.json()
        for a in assignments:
            due = a.get('due_at')
            if due:
                due_date = datetime.fromisoformat(due.replace('Z', '+00:00'))
                if now <= due_date <= one_week:
                    upcoming.append({
                        "course": course['name'],
                        "name": a['name'],
                        "due": due_date.isoformat()
                    })
    return jsonify(upcoming)

@app.route("/gpa")
def get_gpa():
    """Calculate GPA; ?quarter=all or ?quarter=1,2,3,4"""
    quarter = request.args.get("quarter", "all")
    r = requests.get(f"{CANVAS_API_URL}/courses", headers=HEADERS)
    courses = r.json()
    total_points = 0
    total_credits = 0

    for c in courses:
        grade = c.get("current_grade")
        credits = c.get("credits", 1)

        # Example: grades_by_quarter dict in Canvas API
        if quarter != "all":
            grade = c.get("grades_by_quarter", {}).get(quarter, None)

        if grade is not None:
            total_points += float(grade) * credits
            total_credits += credits

    gpa = round(total_points / total_credits, 2) if total_credits else None
    return jsonify({"gpa": gpa})

if __name__ == "__main__":
    app.run(debug=True)
