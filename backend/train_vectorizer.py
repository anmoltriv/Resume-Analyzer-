from pathlib import Path

import joblib

from backend.config import settings
from backend.extractor.pdf_extractor import PDFExtractor
from backend.features.tfidf_engine import TfidfEngine
from backend.preprocessing.boilerplate_remover import BoilerplateRemover
from backend.preprocessing.cleaner import TextCleaner
from backend.preprocessing.lemmatizer import Lemmatizer
from backend.preprocessing.pipeline import PreprocessingPipeline
from backend.preprocessing.tokenizer import Tokenizer


def train_vectorizer(jd_dir: str = "backend/data/jds") -> None:
    extractor = PDFExtractor()
    pipeline = PreprocessingPipeline(TextCleaner(), Tokenizer(), Lemmatizer(), BoilerplateRemover())
    engine = TfidfEngine(settings.vectorizer_path)

    jd_paths = sorted(Path(jd_dir).glob("*.pdf"))[:20]
    if not jd_paths:
        raise RuntimeError("No JD PDFs found for training")

    raw_docs = [extractor.extract(path.read_bytes()) for path in jd_paths]
    processed_docs = [pipeline.process(doc) for doc in raw_docs]

    engine.fit(processed_docs)
    vectors = engine.transform(processed_docs)
    engine.save()

    Path(settings.jd_store_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"paths": [str(p) for p in jd_paths], "vectors": vectors}, settings.jd_store_path)


if __name__ == "__main__":
    train_vectorizer()
