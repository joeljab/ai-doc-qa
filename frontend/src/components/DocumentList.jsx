import React from "react";

export default function DocumentList({ docs, selectedId, onSelect }) {
  return (
    <div className="doc-panel">
      <div className="panel-header">
        <h3>Documents</h3>
        <span className="panel-meta">{docs.length} total</span>
      </div>
      <div className="doc-list">
        {docs.length === 0 && (
          <div className="empty-state">No documents yet. Upload one to begin.</div>
        )}
        {docs.map((d) => (
          <button
            key={d.doc_id}
            type="button"
            onClick={() => onSelect(d.doc_id)}
            className={`doc-item ${d.doc_id === selectedId ? "is-active" : ""}`}
          >
            <div className="doc-title">{d.filename}</div>
            <div className="doc-meta">{d.doc_id}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
