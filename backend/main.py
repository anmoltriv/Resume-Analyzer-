import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import build_routes
from backend.config import settings
from backend.extractor.jd_extractor import JDExtractor
from backend.extractor.ocr_extractor import OCRExtractor
from backend.extractor.pdf_extractor import PDFExtractor
from backend.extractor.url_extractor import URLExtractor
from backend.features.keyword_engine import KeywordEngine
from backend.features.tfidf_engine import TfidfEngine
from backend.preprocessing.boilerplate_remover import BoilerplateRemover
from backend.preprocessing.cleaner import TextCleaner
from backend.preprocessing.lemmatizer import Lemmatizer
from backend.preprocessing.pipeline import PreprocessingPipeline
from backend.preprocessing.role_segmenter import RoleSegmenter
from backend.preprocessing.structure_parser import StructureParser
from backend.preprocessing.tokenizer import Tokenizer
from backend.scoring.cosine_scorer import CosineScorer
from backend.scoring.gemini_scorer import GeminiScorer
from backend.scoring.hybrid_scorer import HybridScorer
from backend.scoring.structure_scorer import StructureScorer
from backend.services.ml_analyzer import AnalyzerDependencies, MLAnalyzerService

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Resume Analyzer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def enforce_content_length(request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > (settings.max_upload_size * 2) + (1024 * 1024):
        raise HTTPException(status_code=413, detail="Request payload too large")
    return await call_next(request)


def build_analyzer_service() -> MLAnalyzerService:
    deps = AnalyzerDependencies(
        jd_extractor=JDExtractor(PDFExtractor(), OCRExtractor(), URLExtractor()),
        pipeline=PreprocessingPipeline(TextCleaner(), Tokenizer(), Lemmatizer(), BoilerplateRemover()),
        role_segmenter=RoleSegmenter(),
        structure_parser=StructureParser(),
        tfidf_engine=TfidfEngine(settings.vectorizer_path),
        keyword_engine=KeywordEngine(),
        structure_scorer=StructureScorer(),
        cosine_scorer=CosineScorer(),
        gemini_scorer=GeminiScorer(settings.gemini_enabled, settings.gemini_api_key),
        hybrid_scorer=HybridScorer(),
    )
    return MLAnalyzerService(deps)


analyzer_service = build_analyzer_service()
app.include_router(build_routes(analyzer_service, settings.max_upload_size))
