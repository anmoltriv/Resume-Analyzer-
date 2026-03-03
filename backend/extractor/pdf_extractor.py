import io

import fitz


class PDFExtractor:
    def extract(self, file_bytes: bytes) -> str:
        document = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")
        try:
            return "\n".join(page.get_text() for page in document).strip()
        finally:
            document.close()
