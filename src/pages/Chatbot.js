import { useState } from "react";

export default function Chatbot() {
  const [chat, setChat] = useState([]);
  const [input, setInput] = useState("");

  const send = () => {
    let response = "Unknown";

    if (input.includes("candidates")) {
      response = "Fetching candidates...";
    }

    setChat([...chat, "You: " + input, "Bot: " + response]);
    setInput("");
  };

  return (
    <div>
      <h2>HR Chatbot</h2>

      <div>
        {chat.map((c, i) => (
          <p key={i}>{c}</p>
        ))}
      </div>

      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}