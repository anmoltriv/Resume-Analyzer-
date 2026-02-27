from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.models.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.feedback_generator import generate_suggestions
from backend.services.keyword_extractor import extract_keywords
from backend.services.scoring_engine import calculate_match
from backend.services.text_preprocessor import preprocess_text

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
def analyze_resume_jd(payload: AnalyzeRequest) -> AnalyzeResponse:
    resume_tokens = preprocess_text(payload.resume_text)
    jd_tokens = preprocess_text(payload.jd_text)
    jd_keywords = extract_keywords(jd_tokens)

    if not resume_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text does not contain analyzable keywords.",
        )

    if not jd_keywords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description does not contain analyzable keywords.",
        )

    try:
        match_score, matched_keywords, missing_keywords = calculate_match(resume_tokens, jd_keywords)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error

    suggestions = generate_suggestions(match_score, missing_keywords)

    return AnalyzeResponse(
        match_score=round(match_score, 4),
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        suggestions=suggestions,
    )
