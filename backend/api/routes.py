from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.services.ml_analyzer import MLAnalyzerService


router = APIRouter()


def build_routes(analyzer: MLAnalyzerService, max_upload_size: int) -> APIRouter:
    @router.post("/analyze")
    async def analyze(
        resume_pdf: UploadFile = File(...),
        jd_pdf: UploadFile | None = File(default=None),
        jd_url: str | None = Form(default=None),
        jd_type: str = Form(...),
    ):
        if resume_pdf.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="resume_pdf must be a PDF")

        resume_bytes = await resume_pdf.read()
        if len(resume_bytes) > max_upload_size:
            raise HTTPException(status_code=413, detail="resume_pdf too large")

        jd_bytes = None
        if jd_type in {"pdf", "image_pdf"}:
            if jd_pdf is None or jd_pdf.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="jd_pdf must be provided as PDF")
            jd_bytes = await jd_pdf.read()
            if len(jd_bytes) > max_upload_size:
                raise HTTPException(status_code=413, detail="jd_pdf too large")

        if jd_type == "url" and not jd_url:
            raise HTTPException(status_code=400, detail="jd_url is required for jd_type=url")

        resume_text = analyzer.deps.jd_extractor.pdf_extractor.extract(resume_bytes)
        return analyzer.analyze(resume_text=resume_text, jd_type=jd_type, jd_file=jd_bytes, jd_url=jd_url)

    return router
