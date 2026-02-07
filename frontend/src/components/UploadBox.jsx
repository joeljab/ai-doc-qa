import React, { useRef } from "react";
import { api } from "../api";

export default function UploadBox({ onUploaded }) {
  const inputRef = useRef(null);

  const uploadFile = async (file) => {
    const form = new FormData();
    form.append("file", file);
    const res = await api.post("/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    onUploaded(res.data);
  };

  return (
    <div
      className="upload-card"
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        const file = e.dataTransfer.files?.[0];
        if (file) uploadFile(file);
      }}
    >
      <div className="upload-content">
        <div>
          <p className="upload-title">Drag and drop a file</p>
          <p className="upload-subtitle">PDF, TXT, or DOCX up to 20 MB</p>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => inputRef.current?.click()}
        >
          Choose file
        </button>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt,.docx"
        style={{ display: "none" }}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) uploadFile(file);
        }}
      />
    </div>
  );
}
