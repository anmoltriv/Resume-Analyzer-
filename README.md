# Resume Analyzer Backend (Modular ML Engine)

FastAPI backend for deterministic resume ↔ JD matching with optional Gemini augmentation.

## API

- `POST /analyze`
- Multipart fields:
  - `resume_pdf` (required PDF)
  - `jd_type` (`pdf`, `image_pdf`, `url`)
  - `jd_pdf` (required when type is `pdf` / `image_pdf`)
  - `jd_url` (required when type is `url`)

Returns weighted hybrid scoring with explainability fields and per-role breakdown.

## Training

```bash
python backend/train_vectorizer.py
```

This fits TF-IDF on up to 20 JD PDFs under `backend/data/jds`, then persists:
- `backend/models/vectorizer.pkl`
- `backend/models/jd_vector_store.pkl`

## Run

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
