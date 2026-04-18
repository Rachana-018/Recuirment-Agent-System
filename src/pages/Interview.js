import { useState } from "react";

export default function Interview() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [ws, setWs] = useState(null);

  const startInterview = () => {
    const socket = new WebSocket("ws://localhost:8000/ws/interview");

    socket.onmessage = (event) => {
      setMessages((prev) => [...prev, "Bot: " + event.data]);
    };

    setWs(socket);
  };

  const sendAnswer = () => {
    ws.send(input);
    setMessages((prev) => [...prev, "You: " + input]);
    setInput("");
  };

  return (
    <div>
      <h2>Interview</h2>

      <button onClick={startInterview}>Start</button>

      <div>
        {messages.map((m, i) => (
          <p key={i}>{m}</p>
        ))}
      </div>

      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendAnswer}>Send</button>
    </div>
  );
}