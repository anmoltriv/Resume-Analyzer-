from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEngine:
    def __init__(self, vectorizer_path: str, max_features: int = 5000):
        self.vectorizer_path = Path(vectorizer_path)
        self.vectorizer = self._load_or_create(max_features)

    def _load_or_create(self, max_features: int) -> TfidfVectorizer:
        if self.vectorizer_path.exists():
            return joblib.load(self.vectorizer_path)
        return TfidfVectorizer(ngram_range=(1, 2), max_features=max_features, stop_words="english")

    def fit(self, documents: list[str]):
        self.vectorizer.fit(documents)

    def transform(self, documents: list[str]):
        return self.vectorizer.transform(documents)

    def save(self) -> None:
        self.vectorizer_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, self.vectorizer_path)

    def get_feature_names(self) -> list[str]:
        return list(self.vectorizer.get_feature_names_out())
