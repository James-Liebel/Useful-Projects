import React, { useEffect, useState } from "react";
import axios from "axios";
import Courses from "./Courses";
import GPA from "./GPA";
import UpcomingAssignments from "./UpcomingAssignments";

export default function Dashboard() {
  const [courses, setCourses] = useState([]);
  const [gpa, setGpa] = useState(null);
  const [upcoming, setUpcoming] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/courses")
      .then(res => setCourses(res.data));
    axios.get("http://127.0.0.1:5000/api/gpa")
      .then(res => setGpa(res.data.gpa));
    axios.get("http://127.0.0.1:5000/api/upcoming")
      .then(res => setUpcoming(res.data));
  }, []);

  return (
    <div>
      <GPA gpa={gpa} />
      <UpcomingAssignments assignments={upcoming} />
      <Courses courses={courses} />
    </div>
  );
}
