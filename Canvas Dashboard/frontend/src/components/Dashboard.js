import React, { useState, useEffect } from "react";

const Dashboard = () => {
  const [gpa, setGpa] = useState(null);
  const [courses, setCourses] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [quarter, setQuarter] = useState("All");
  const [quarters, setQuarters] = useState(["All"]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:5000/courses?quarter=${quarter}`);
      const data = await response.json();
      setGpa(data.gpa);
      setCourses(data.courses);
      setAssignments(data.upcoming_assignments);
      if (data.quarters) setQuarters(data.quarters);
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [quarter]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Canvas Grades Dashboard</h1>

      <div>
        <h2>Current GPA</h2>
        <p>{gpa !== null ? gpa : "N/A"}</p>
      </div>

      <div>
        <h2>Quarter:</h2>
        <select value={quarter} onChange={(e) => setQuarter(e.target.value)}>
          {quarters.map((q) => (
            <option key={q} value={q}>
              {q}
            </option>
          ))}
        </select>
      </div>

      <div>
        <h2>Upcoming Assignments (Next 7 Days)</h2>
        {loading ? (
          <p>Loading...</p>
        ) : assignments.length === 0 ? (
          <p>No upcoming assignments.</p>
        ) : (
          <ul>
            {assignments.map((a) => (
              <li key={a.course_id + a.name}>
                {a.name} — due {new Date(a.due_at).toLocaleString()}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h2>Courses</h2>
        {loading ? (
          <p>Loading...</p>
        ) : courses.length === 0 ? (
          <p>No courses found.</p>
        ) : (
          <ul>
            {courses.map((c) => (
              <li key={c.id}>
                {c.name} — Grade: {c.grade || "N/A"}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
