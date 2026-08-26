from fastapi import FastAPI

app = FastAPI(
    title="IntelliScan API",
    description="Backend API for Offline Multimodal Edge AI",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "IntelliScan API is running",
        "status": "ok",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "intelliscan-backend",
    }


@app.get("/api/test")
async def test():
    return {
        "message": "FastAPI test successful",
        "backend": "FastAPI",
        "device": "Raspberry Pi",
    }
