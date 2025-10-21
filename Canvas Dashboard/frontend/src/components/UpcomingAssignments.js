// frontend/src/components/UpcomingAssignments.js
import React, { useEffect, useState } from "react";

const UpcomingAssignments = () => {
  const [assignments, setAssignments] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/assignments/next_week")
      .then(res => res.json())
      .then(data => setAssignments(data))
      .catch(console.error);
  }, []);

  return (
    <div style={{ marginBottom: "20px" }}>
      <h2>Upcoming Assignments (Next 7 Days)</h2>
      {assignments.length === 0 && <p>No upcoming assignments.</p>}
      <ul>
        {assignments.map((a, i) => (
          <li key={i}>
            {a.course}: {a.name} — due {new Date(a.due).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UpcomingAssignments;
