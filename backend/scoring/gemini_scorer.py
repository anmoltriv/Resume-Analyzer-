import logging
import os
import re

import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiScorer:
    def __init__(self, enabled: bool, api_key: str | None):
        self.enabled = enabled and bool(api_key)
        if self.enabled:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        else:
            self.model = None

    def score(self, resume_text: str, jd_text: str) -> float:
        if not self.enabled or not self.model:
            return 0.0

        prompt = (
            "Return only a number from 0 to 4 for resume-job alignment.\n"
            f"Resume:\n{resume_text}\n\nJob Description:\n{jd_text}"
        )
        try:
            response = self.model.generate_content(prompt, generation_config={"temperature": 0})
            raw = (getattr(response, "text", "") or "").strip()
            match = re.search(r"\d+(?:\.\d+)?", raw)
            if not match:
                return 0.0
            value = float(match.group(0))
            return round(max(0.0, min(4.0, value)), 2)
        except Exception as exc:
            logger.warning("Gemini scoring failed: %s", exc)
            return 0.0
