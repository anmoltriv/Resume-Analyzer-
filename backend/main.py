from __future__ import annotations

from fastapi import FastAPI

from backend.routes.analyze import router as analyze_router

app = FastAPI(
    title="Resume vs JD Analyzer API",
    version="1.0.0",
    description="Deterministic keyword-based resume and job description matching service.",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(analyze_router)
