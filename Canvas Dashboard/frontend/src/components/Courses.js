import React from "react";

export default function Courses({ courses }) {
  return (
    <div className="mb-4">
      <h2 className="text-xl font-semibold mb-2">Courses</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {courses.map(c => (
          <div key={c.id} className="p-4 border rounded-lg shadow-sm">
            <h3 className="font-semibold">{c.name}</h3>
            <p>Grade: {c.grade !== null ? c.grade.toFixed(2) : "N/A"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
