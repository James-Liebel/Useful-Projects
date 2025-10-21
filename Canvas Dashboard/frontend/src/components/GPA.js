// frontend/src/components/GPA.js
import React, { useEffect, useState } from "react";

const GPA = () => {
  const [gpa, setGpa] = useState("N/A");
  const [quarter, setQuarter] = useState("all");

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/gpa?quarter=${quarter}`)
      .then(res => res.json())
      .then(data => setGpa(data.gpa || "N/A"))
      .catch(console.error);
  }, [quarter]);

  return (
    <div style={{ marginBottom: "20px" }}>
      <h2>Current GPA</h2>
      <p>{gpa}</p>
      <label>
        Quarter:
        <select value={quarter} onChange={e => setQuarter(e.target.value)}>
          <option value="all">All</option>
          <option value="1">Quarter 1</option>
          <option value="2">Quarter 2</option>
          <option value="3">Quarter 3</option>
          <option value="4">Quarter 4</option>
        </select>
      </label>
    </div>
  );
};

export default GPA;
