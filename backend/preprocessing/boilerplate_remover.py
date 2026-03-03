import re


class BoilerplateRemover:
    PATTERNS = [
        r"references available upon request",
        r"curriculum vitae",
        r"resume",
    ]

    def remove(self, text: str) -> str:
        cleaned = text
        for pattern in self.PATTERNS:
            cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", cleaned).strip()
