// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from "react";
import UpcomingAssignments from "./UpcomingAssignments";
import GPA from "./GPA";

const Dashboard = () => {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/courses")
      .then(res => res.json())
      .then(data => setCourses(data))
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Canvas Grades Dashboard</h1>
      <GPA />
      <UpcomingAssignments />
      <h2>Courses</h2>
      {courses.map(c => (
        <div key={c.id}>
          {c.name} - Grade: {c.current_grade || "N/A"}
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
