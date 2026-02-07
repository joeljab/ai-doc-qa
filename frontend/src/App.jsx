import React, { useCallback, useEffect, useState } from "react";
import { api } from "./api";
import UploadBox from "./components/UploadBox";
import DocumentList from "./components/DocumentList";
import Chat from "./components/Chat";
import "./App.css";

export default function App() {
  const [docs, setDocs] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    const loadDocs = async () => {
      try {
        const res = await api.get("/documents");
        setDocs(res.data);
      } catch (err) {
        console.error("Failed to load documents", err);
      }
    };
    loadDocs();
  }, []);

  const refreshDocs = useCallback(async () => {
    try {
      const res = await api.get("/documents");
      setDocs(res.data);
    } catch (err) {
      console.error("Failed to load documents", err);
    }
  }, []);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="app-eyebrow">Doc Intelligence</p>
          <h1 className="app-title">ASKDoc</h1>
          <p className="app-subtitle">
            Upload a document, then ask precise questions with traceable answers.
          </p>
        </div>
        <div className="app-badge">
          <span className="app-badge-dot" />
          Ready
        </div>
      </header>

      <section className="panel panel-delay-1">
        <UploadBox onUploaded={() => refreshDocs()} />
      </section>

      <section className="app-grid">
        <div className="panel panel-delay-2">
          <DocumentList docs={docs} selectedId={selectedId} onSelect={setSelectedId} />
        </div>
        <div className="panel panel-delay-3">
          <Chat docId={selectedId} />
        </div>
      </section>
    </div>
  );
}
