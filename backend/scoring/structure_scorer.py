import re


class StructureScorer:
    CHECKS = {
        "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "linkedin": r"linkedin\.com/",
        "github": r"github\.com/",
        "skills": r"\bskills\b",
        "experience": r"\bexperience\b",
        "projects": r"\bprojects?\b",
    }

    def score(self, resume_text: str) -> float:
        matches = sum(bool(re.search(pattern, resume_text, flags=re.IGNORECASE)) for pattern in self.CHECKS.values())
        return round((matches / len(self.CHECKS)) * 2.0, 2)
