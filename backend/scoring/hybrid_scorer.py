import logging

logger = logging.getLogger(__name__)


class HybridScorer:
    def combine(self, structure_score: float, cosine_score: float, gemini_score: float) -> dict:
        final_score = structure_score + cosine_score + gemini_score
        logger.info(
            "score_components structure=%.2f cosine=%.2f gemini=%.2f final=%.2f",
            structure_score,
            cosine_score,
            gemini_score,
            final_score,
        )
        return {
            "structure_score": structure_score,
            "cosine_score": cosine_score,
            "gemini_score": gemini_score,
            "overall_score": round(final_score * 10),
        }
