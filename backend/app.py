from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import logging

from dotenv import load_dotenv
load_dotenv()


from config import Config

try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
except Exception:  # optional dependency
    AzureLogHandler = None
from services.blob_service import BlobStorage
from services.extract_text import extract_text
from services.chunking import chunk_text
from services.embeddings import AOAI
from services.search_index import create_index_if_missing, get_search_client, upsert_chunks
from services.rag import retrieve_top_chunks, build_prompt

app = Flask(__name__)
CORS(app)

cfg = Config()

if cfg.AZURE_APPINSIGHTS_CONNECTION_STRING:
    if AzureLogHandler is None:
        print("App Insights connection string set, but opencensus-ext-azure is not installed.")
    else:
        level_name = (cfg.AZURE_APPINSIGHTS_LOG_LEVEL or "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        handler = AzureLogHandler(connection_string=cfg.AZURE_APPINSIGHTS_CONNECTION_STRING)
        handler.setLevel(level)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(level)
        app.logger.addHandler(handler)
        app.logger.setLevel(level)

# Init services
blob = BlobStorage(cfg.AZURE_BLOB_CONNECTION_STRING or "", cfg.AZURE_BLOB_CONTAINER or "")
aoai = AOAI(
    endpoint=cfg.AZURE_OPENAI_ENDPOINT or "",
    api_key=cfg.AZURE_OPENAI_API_KEY or "",
    api_version=cfg.AZURE_OPENAI_API_VERSION or "",
    chat_deployment=cfg.AZURE_OPENAI_CHAT_DEPLOYMENT or "",
    embedding_deployment=cfg.AZURE_OPENAI_EMBEDDING_DEPLOYMENT or ""
)

create_index_if_missing(cfg.AZURE_SEARCH_ENDPOINT or "", cfg.AZURE_SEARCH_API_KEY or "", cfg.AZURE_SEARCH_INDEX_NAME or "")
search_client = get_search_client(cfg.AZURE_SEARCH_ENDPOINT or "", cfg.AZURE_SEARCH_API_KEY or "", cfg.AZURE_SEARCH_INDEX_NAME or "")

# simple in-memory registry for demo (replace with DB later)
DOCUMENTS = {}  # doc_id -> {filename, blob_name}

@app.post("/upload")
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Missing file"}), 400

        f = request.files["file"]
        filename = f.filename or "uploaded"
        file_bytes = f.read()

        print("UPLOAD: received", filename, "bytes:", len(file_bytes))

        blob_name = blob.upload_file(file_bytes, filename)
        print("UPLOAD: blob stored as", blob_name)

        text = extract_text(file_bytes, filename)
        print("UPLOAD: extracted text length", len(text))

        if not text.strip():
            return jsonify({"error": "Could not extract text"}), 400

        chunks = chunk_text(text)
        print("UPLOAD: chunks", len(chunks))

        vectors = aoai.embed(chunks)
        print("UPLOAD: embedded", len(vectors))

        doc_id = str(uuid.uuid4())
        DOCUMENTS[doc_id] = {"filename": filename, "blob_name": blob_name}

        records = []
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            records.append({
                "id": f"{doc_id}_{i}",
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": i,
                "content": chunk,
                "contentVector": vec
            })

        upsert_chunks(search_client, records)
        print("UPLOAD: indexed records", len(records))

        return jsonify({"doc_id": doc_id, "filename": filename, "chunks_indexed": len(records)})

    except Exception as e:
        import traceback
        print("UPLOAD ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.get("/documents")
def documents():
    items = [{"doc_id": k, **v} for k, v in DOCUMENTS.items()]
    return jsonify(items)

@app.post("/ask")
def ask():
    data = request.get_json(force=True)
    doc_id = data.get("doc_id")
    question = data.get("question")

    if not doc_id or doc_id not in DOCUMENTS:
        return jsonify({"error": "Invalid doc_id"}), 400
    if not question:
        return jsonify({"error": "Missing question"}), 400

    qvec = aoai.embed([question])[0]
    top_chunks = retrieve_top_chunks(search_client, qvec, doc_id, k=5)

    prompt = build_prompt(question, top_chunks)
    answer = aoai.chat(
        system_prompt="You are a helpful assistant that answers strictly from context.",
        user_prompt=prompt
    )

    return jsonify({"answer": answer, "sources_count": len(top_chunks)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=cfg.PORT, debug=True)
