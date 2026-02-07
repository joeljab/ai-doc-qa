# AI Document Q&A

<img width="3840" height="2160" alt="image" src="https://github.com/user-attachments/assets/3e2843dd-264e-43af-b922-ad27d188448c" />


Minimal setup guide for the demo app.

## Prerequisites
- Python 3.10+
- Node.js 18+

## Backend (Flask)
1. Create a venv and install deps:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
   - `pip install -r backend/requirements.txt`
   -   - Optional: set `AZURE_APPINSIGHTS_CONNECTION_STRING` to enable logging.
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
