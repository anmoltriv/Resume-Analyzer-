from __future__ import annotations

from typing import List, Set, Tuple


def calculate_match(
    resume_tokens: List[str],
    jd_keywords: List[str],
) -> Tuple[float, List[str], List[str]]:
    """Calculate deterministic keyword match score and keyword coverage."""
    if not jd_keywords:
        raise ValueError("No valid JD keywords available for scoring.")

    resume_token_set: Set[str] = set(resume_tokens)
    matched_keywords: List[str] = [keyword for keyword in jd_keywords if keyword in resume_token_set]
    missing_keywords: List[str] = [keyword for keyword in jd_keywords if keyword not in resume_token_set]

    match_score: float = len(matched_keywords) / len(jd_keywords)
    return match_score, matched_keywords, missing_keywords
