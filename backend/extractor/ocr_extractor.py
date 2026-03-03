import io

import fitz


class OCRExtractor:
    def extract(self, file_bytes: bytes) -> str:
        try:
            import pytesseract
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("OCR dependencies not installed: pytesseract/Pillow") from exc

        document = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")
        pages: list[str] = []
        try:
            for page in document:
                pix = page.get_pixmap(dpi=200)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                pages.append(pytesseract.image_to_string(image))
        finally:
            document.close()
        return "\n".join(pages).strip()
