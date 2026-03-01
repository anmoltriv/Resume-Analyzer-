import io
import os
import re
from typing import Optional

import fitz
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_ORIGINS = ["http://localhost:5173"]

app = FastAPI(title="Resume Analyzer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def enforce_content_length(request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > (MAX_UPLOAD_SIZE * 2) + (1024 * 1024):
        raise HTTPException(status_code=413, detail="Request payload too large")
    return await call_next(request)


def extract_pdf_text(file_bytes: bytes) -> str:
    if len(file_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Each PDF must be 10MB or less")

    try:
        document = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid PDF file") from exc

    extracted_pages = [page.get_text() for page in document]
    document.close()
    text = "\n".join(extracted_pages).strip()

    if not text:
        raise HTTPException(status_code=400, detail="Uploaded PDF has no extractable text")

    return text


def parse_score(raw_response: str) -> Optional[int]:
    text = raw_response.strip()

    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        numeric = int(round(float(text)))
        return max(0, min(10, numeric))

    match = re.search(r"-?\d+", text)
    if match:
        numeric = int(match.group(0))
        return max(0, min(10, numeric))

    return None


def evaluate_with_gemini(resume_text: str, jd_text: str) -> int:
    for m in genai.list_models():
        print(m.name, m.supported_generation_methods)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured")

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are a strict resume evaluator.\n"
            "Return ONLY a number between 0 and 10.\n"
            "Do not explain anything.\n"
            "Do not output text.\n"
            "Only return the number."
        ),
    )

    user_prompt = (
        "Evaluate how well the following resume fits the job description.\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{jd_text}"
    )

    try:
        response = model.generate_content(
            user_prompt,
            generation_config={"temperature": 0},
        )
    except Exception as exc:
        print("Gemini exception:", repr(exc))
        raise

    raw_output = getattr(response, "text", "") or ""
    score = parse_score(raw_output)

    if score is None:
        raise HTTPException(status_code=502, detail="Gemini returned an invalid score format")

    return score


@app.post("/evaluate")
async def evaluate_resume(
    resume_pdf: UploadFile = File(...),
    jd_pdf: UploadFile = File(...),
):
    if resume_pdf.content_type != "application/pdf" or jd_pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Both files must be PDFs")

    resume_bytes = await resume_pdf.read()
    jd_bytes = await jd_pdf.read()

    resume_text = extract_pdf_text(resume_bytes)
    jd_text = extract_pdf_text(jd_bytes)

    score = evaluate_with_gemini(resume_text, jd_text)
    return {"score": score}
