from __future__ import annotations

from typing import List


def generate_suggestions(match_score: float, missing_keywords: List[str]) -> List[str]:
    """Generate suggestions based on threshold-based scoring bands."""
    suggestions: List[str] = []

    if match_score < 0.4:
        suggestions.append(
            "Low match: add missing skills explicitly in your resume summary and experience bullets."
        )
        if missing_keywords:
            suggestions.append(
                f"Prioritize adding these missing keywords where applicable: {', '.join(missing_keywords[:10])}."
            )
    elif match_score < 0.7:
        suggestions.append(
            "Moderate match: strengthen depth of experience in the matched skill areas with measurable outcomes."
        )
    else:
        suggestions.append(
            "Strong match: tailor resume bullet points to mirror the job description phrasing and priorities."
        )

    return suggestions
