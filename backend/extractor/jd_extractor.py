from backend.extractor.ocr_extractor import OCRExtractor
from backend.extractor.pdf_extractor import PDFExtractor
from backend.extractor.url_extractor import URLExtractor


class JDExtractor:
    def __init__(self, pdf_extractor: PDFExtractor, ocr_extractor: OCRExtractor, url_extractor: URLExtractor):
        self.pdf_extractor = pdf_extractor
        self.ocr_extractor = ocr_extractor
        self.url_extractor = url_extractor

    def extract_jd(self, input_type: str, file: bytes | None = None, url: str | None = None) -> str:
        if input_type == "pdf" and file:
            return self.pdf_extractor.extract(file)
        if input_type == "image_pdf" and file:
            return self.ocr_extractor.extract(file)
        if input_type == "url" and url:
            return self.url_extractor.extract(url)
        raise ValueError("Invalid JD input parameters")
