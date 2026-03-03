from dataclasses import dataclass

from backend.extractor.jd_extractor import JDExtractor
from backend.features.keyword_engine import KeywordEngine
from backend.features.tfidf_engine import TfidfEngine
from backend.preprocessing.pipeline import PreprocessingPipeline
from backend.preprocessing.role_segmenter import RoleSegmenter
from backend.preprocessing.structure_parser import StructureParser
from backend.scoring.cosine_scorer import CosineScorer
from backend.scoring.gemini_scorer import GeminiScorer
from backend.scoring.hybrid_scorer import HybridScorer
from backend.scoring.structure_scorer import StructureScorer


@dataclass
class AnalyzerDependencies:
    jd_extractor: JDExtractor
    pipeline: PreprocessingPipeline
    role_segmenter: RoleSegmenter
    structure_parser: StructureParser
    tfidf_engine: TfidfEngine
    keyword_engine: KeywordEngine
    structure_scorer: StructureScorer
    cosine_scorer: CosineScorer
    gemini_scorer: GeminiScorer
    hybrid_scorer: HybridScorer


class MLAnalyzerService:
    def __init__(self, deps: AnalyzerDependencies):
        self.deps = deps

    def analyze(self, resume_text: str, jd_type: str, jd_file: bytes | None = None, jd_url: str | None = None):
        jd_text = self.deps.jd_extractor.extract_jd(jd_type, file=jd_file, url=jd_url)
        processed_resume = self.deps.pipeline.process(resume_text)
        role_segments = self.deps.role_segmenter.segment(jd_text)
        role_results = []

        for role in role_segments:
            processed_role = self.deps.pipeline.process(role)
            vectors = self.deps.tfidf_engine.transform([processed_resume, processed_role])
            resume_vector, role_vector = vectors[0], vectors[1]
            structure_score = self.deps.structure_scorer.score(resume_text)
            cosine_score = self.deps.cosine_scorer.score(resume_vector, role_vector)
            gemini_score = self.deps.gemini_scorer.score(resume_text, role)
            combined = self.deps.hybrid_scorer.combine(structure_score, cosine_score, gemini_score)

            features = self.deps.tfidf_engine.get_feature_names()
            resume_keywords = self.deps.keyword_engine.extract_top_keywords(resume_vector, features)
            role_keywords = self.deps.keyword_engine.extract_top_keywords(role_vector, features)
            missing = self.deps.keyword_engine.missing_keywords(resume_keywords, role_keywords)
            role_results.append(
                {
                    "role_name": role.splitlines()[0][:80],
                    **combined,
                    "top_keywords": role_keywords,
                    "missing_keywords": missing,
                }
            )

        best = max(role_results, key=lambda item: item["overall_score"])
        return {
            "overall_score": best["overall_score"],
            "best_matching_role": best["role_name"],
            "structure_score": best["structure_score"],
            "cosine_score": best["cosine_score"],
            "gemini_score": best["gemini_score"],
            "top_keywords": best["top_keywords"],
            "missing_keywords": best["missing_keywords"],
            "section_scores": self.deps.structure_parser.extract_section_scores(resume_text),
            "per_role_scores": role_results,
        }
