from fastapi import APIRouter, Response
from api.inference import camera_service
from fastapi.responses import StreamingResponse
from pathlib import Path 


router = APIRouter(
    prefix= "/api/camera",
    tags=["camera"],
)


INSPECTION_IMAGE = Path(
    "/home/intelliscan/Documents/intelliscan/"
    "data/captures/latest_inspection.jpg"
)


@router.get("/frame")
def get_frame():
    "Return the current camea as a JPEG."

    frame = camera_service.capture_frame()

    return Response(
        content = frame,
        media_type = "image/jpeg",
    )

@router.get("/stream")
def camera_stream():
    return StreamingResponse(
        camera_service.generate_frames(),
        media_type=(
            "multipart/x-mixed-replace; "
            "boundary=frame"

        ),
    )

@router.get("/inspection")
def get_inspection_image():
    """Return the last image that was sent to Gemma."""
    if not INSPECTION_IMAGE.exists():
        return Response(
            content=b"Inspection image not available.",
            status_code=404,
            media_type="text/plain",
        )

    return Response(
        content=INSPECTION_IMAGE.read_bytes(),
        media_type="image/jpeg",
    )