# Resume Analyzer MVP

Minimal full-stack project with:
- **Backend:** FastAPI + PyMuPDF + Gemini API
- **Frontend:** React (Vite)

## Project structure

```text
backend/
  main.py
  requirements.txt
  .env.example
frontend/
  index.html
  package.json
  vite.config.js
  src/
    main.jsx
    App.jsx
    styles.css
```

## Backend setup (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# add your GEMINI_API_KEY in .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend endpoint:
- `POST /evaluate`
- Form fields: `resume_pdf`, `jd_pdf`
- Returns: `{ "score": <int> }`

## Frontend setup (React + Vite)

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Open `http://localhost:5173`.
The frontend posts files to `http://localhost:8000/evaluate`.

## Notes

- Max upload size is **10MB per PDF**.
- CORS allows `http://localhost:5173`.
- Gemini model: `gemini-1.5-flash` with `temperature=0`.
