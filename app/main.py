from fastapi import FastAPI

app = FastAPI(
    title="Mock Interview AI",
    description="음성 답변 기반 AI 모의 면접 플랫폼",
    version="0.0.1",
)


@app.get("/")
def root():
    return {
        "service": "Mock Interview AI",
        "status": "under development",
        "version": "0.0.1",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
