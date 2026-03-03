from sklearn.metrics.pairwise import cosine_similarity


class CosineScorer:
    def score(self, resume_vector, jd_vector) -> float:
        similarity = float(cosine_similarity(resume_vector, jd_vector)[0][0])
        return round(max(0.0, min(1.0, similarity)) * 4.0, 2)
