import { useState } from "react";
import API from "../api";

export default function Schedule() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);

  const schedule = async () => {
    const res = await API.post(`/schedule/?email=${email}`);
    setResult(res.data);
  };

  return (
    <div>
      <h2>Schedule Interview</h2>

      <input
        placeholder="Candidate Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button onClick={schedule}>Schedule</button>

      {result && <p>Meeting Link: {result.link}</p>}
    </div>
  );
}