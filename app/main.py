from fastapi import FastAPI
from app.api.v1 import sessions

app = FastAPI(
    title="Mock Interview AI",
    description="음성 답변 기반 AI 모의 면접 플랫폼",
    version="0.1.0",
)

app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])


@app.get("/")
def root():
    return {
        "service": "Mock Interview AI",
        "status": "under development",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}