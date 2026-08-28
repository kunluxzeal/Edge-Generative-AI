from contextlib import asynccontextmanager

from fastapi import FastAPI
from api.inference import gemma_service,camera_service ,router as inference_router
from api.camera import router as camera_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading Gemma 4...")
    load_time = gemma_service.load()
    print(f"Gemma loaded in {load_time:.3f} seconds")

    print("Starting camera...")
    camera_service.start()
    print("Camera started")

    yield


    print("Stopping camera...")
    camera_service.close()


    print("Closing Gemma...")
    gemma_service.close()

    print("Services closed")


app = FastAPI(
    title="IntelliScan API",
    description="Backend API for Offline Multimodal Edge AI",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(inference_router)
app.include_router(camera_router)

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
