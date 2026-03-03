from typing import Optional


class EmbeddingEngine:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.model: Optional[object] = None
        if enabled:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def encode(self, texts: list[str]):
        if not self.enabled or not self.model:
            return None
        return self.model.encode(texts)
