import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ padding: 10, background: "#222", color: "#fff" }}>
      <Link to="/" style={{ margin: 10 }}>Upload</Link>
      <Link to="/dashboard" style={{ margin: 10 }}>Dashboard</Link>
      <Link to="/interview" style={{ margin: 10 }}>Interview</Link>
      <Link to="/schedule" style={{ margin: 10 }}>Schedule</Link>
      <Link to="/chatbot" style={{ margin: 10 }}>Chatbot</Link>
    </nav>
  );
}