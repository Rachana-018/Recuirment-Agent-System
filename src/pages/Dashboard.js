import { useEffect, useState } from "react";
import API from "../api";

export default function Dashboard() {
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    API.get("/candidates/").then((res) => setCandidates(res.data));
  }, []);

  return (
    <div>
      <h2>Candidate Dashboard</h2>

      <table border="1">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Score</th>
            <th>Stage</th>
          </tr>
        </thead>

        <tbody>
          {candidates.map((c) => (
            <tr key={c.id}>
              <td>{c.name}</td>
              <td>{c.email}</td>
              <td>{c.ats_score}</td>
              <td>{c.stage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}