# AI Document Q&A

Minimal setup guide for the demo app.

## Prerequisites
- Python 3.10+
- Node.js 18+

## Backend (Flask)
1. Create a venv and install deps:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
   - `pip install -r backend/requirements.txt`
2. Configure environment:
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in Azure OpenAI, Search, Blob, and Document Intelligence values.
   - Optional: set `AZURE_APPINSIGHTS_CONNECTION_STRING` to enable logging.
3. Run the API:
   - `python backend/app.py`

Backend runs on `http://localhost:5000`.

## Frontend (Vite)
1. Install deps:
   - `npm install`
2. Run dev server:
   - `npm run dev`

Frontend runs on the Vite URL shown in the terminal.
