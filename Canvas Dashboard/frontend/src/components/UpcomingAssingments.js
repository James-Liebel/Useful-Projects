import React from "react";

export default function UpcomingAssignments({ assignments }) {
  return (
    <div className="mb-4 p-4 border rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-2">Upcoming Assignments</h2>
      <ul>
        {assignments.map((a, idx) => (
          <li key={idx} className="mb-1">
            <strong>{a.course}:</strong> {a.name} — due {a.due_at ? new Date(a.due_at).toLocaleString() : "N/A"}
          </li>
        ))}
      </ul>
    </div>
  );
}
