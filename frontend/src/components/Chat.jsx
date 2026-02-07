import React, { useState } from "react";
import { api } from "../api";

export default function Chat({ docId }) {
  const [messages, setMessages] = useState([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!docId || !q.trim()) return;
    const userMsg = { role: "user", content: q };
    setMessages((m) => [...m, userMsg]);
    setQ("");
    setLoading(true);

    try {
      const res = await api.post("/ask", { doc_id: docId, question: userMsg.content });
      setMessages((m) => [...m, { role: "assistant", content: res.data.answer }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-panel">
      <div className="panel-header">
        <h3>Q&A</h3>
        <span className="panel-meta">{messages.length} messages</span>
      </div>
      {!docId && <p className="helper-text">Select a document first.</p>}

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`chat-message ${m.role === "user" ? "from-user" : "from-ai"}`}
          >
            <div className="chat-role">{m.role === "user" ? "You" : "AI"}</div>
            <div className="chat-bubble">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="chat-message from-ai">
            <div className="chat-role">AI</div>
            <div className="chat-bubble">Typing...</div>
          </div>
        )}
      </div>

      <div className="chat-input-row">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask a question..."
          className="input"
          onKeyDown={(e) => e.key === "Enter" && ask()}
          disabled={!docId}
        />
        <button type="button" className="btn btn-secondary" onClick={ask} disabled={!docId}>
          Send
        </button>
      </div>
    </div>
  );
}
