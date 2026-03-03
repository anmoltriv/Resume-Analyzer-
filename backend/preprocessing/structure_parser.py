import re


class StructureParser:
    def extract_section_scores(self, resume_text: str) -> dict[str, int]:
        text = resume_text.lower()
        weights = {
            "skills": ["skills", "technologies", "tools"],
            "experience": ["experience", "employment", "work history"],
            "education": ["education", "degree", "university"],
        }
        scores: dict[str, int] = {}
        for section, patterns in weights.items():
            matches = sum(bool(re.search(rf"\b{re.escape(pattern)}\b", text)) for pattern in patterns)
            scores[section] = int((matches / len(patterns)) * 100)
        return scores
