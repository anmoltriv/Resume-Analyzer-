# Resume vs Job Description Analyzer (FastAPI)

A production-ready, deterministic backend service that compares a resume against a job description using keyword-based scoring.

## Features

- FastAPI-based REST API
- Deterministic scoring (no ML/LLM/embeddings)
- Modular service architecture
- Input validation and error handling

## Project Structure

```text
backend/
 ├── main.py
 ├── routes/
 │     └── analyze.py
 ├── services/
 │     ├── text_preprocessor.py
 │     ├── keyword_extractor.py
 │     ├── scoring_engine.py
 │     └── feedback_generator.py
 ├── models/
 │     └── schemas.py
 ├── requirements.txt
 └── README.md
```

## API

### `POST /analyze`

Request:

```json
{
  "resume_text": "string",
  "jd_text": "string"
}
```

Response:

```json
{
  "match_score": 0.5,
  "matched_keywords": ["python", "fastapi"],
  "missing_keywords": ["docker", "aws"],
  "suggestions": [
    "Moderate match: strengthen depth of experience in the matched skill areas with measurable outcomes."
  ]
}
```

## Local Run

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run the API server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Open docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes on Scoring

1. Text preprocessing:
   - lowercasing
   - punctuation removal
   - stopword removal
   - tokenization
2. JD keywords are extracted by token frequency and de-duplicated.
3. `match_score = matched_jd_keywords / total_jd_keywords`
4. Suggestions are returned based on score bands:
   - `< 0.4`
   - `0.4 <= score < 0.7`
   - `>= 0.7`
