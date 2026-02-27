from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., description="Raw resume text")
    jd_text: str = Field(..., description="Raw job description text")

    @field_validator("resume_text", "jd_text")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty.")
        return value


class AnalyzeResponse(BaseModel):
    match_score: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
