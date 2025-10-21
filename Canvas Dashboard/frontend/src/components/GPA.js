import React from "react";

export default function GPA({ gpa }) {
  return (
    <div className="mb-4 p-4 border rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold">Current GPA</h2>
      <p className="text-2xl">{gpa}</p>
    </div>
  );
}
