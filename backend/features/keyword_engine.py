class KeywordEngine:
    def extract_top_keywords(self, vector, feature_names: list[str], top_n: int = 15) -> list[str]:
        dense = vector.toarray().ravel().tolist()
        indices = sorted(range(len(dense)), key=lambda idx: dense[idx], reverse=True)
        return [feature_names[idx] for idx in indices[:top_n] if dense[idx] > 0]

    def missing_keywords(self, resume_keywords: list[str], jd_keywords: list[str]) -> list[str]:
        resume_set = set(resume_keywords)
        return [keyword for keyword in jd_keywords if keyword not in resume_set]
