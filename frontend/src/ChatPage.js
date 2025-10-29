import React, { useState } from "react";
import axios from "axios";

function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    const userMsg = { sender: "user", text: message };
    setChat((prev) => [...prev, userMsg]);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { message });
      const botMsg = {
        sender: "bot",
        text: res.data.response,
        sentiment: res.data.sentiment,
      };
      setChat((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      setMessage("");
    }
  };

  return (
    <div className="chat-container">
      <h1>🧠 AI Mental Health Assistant</h1>

      <div className="chat-box">
        {chat.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-msg ${msg.sender === "user" ? "user" : "bot"}`}
          >
            <p>{msg.text}</p>
            {msg.sentiment && (
              <span className="sentiment">Mood: {msg.sentiment}</span>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage} className="chat-input">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your thoughts…"
        />
        <button type="submit" disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}

export default ChatPage;