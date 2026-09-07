from fastapi import APIRouter, HTTPException

from services.camera_service import CameraService
from services.gemma_service import GemmaService

router = APIRouter(prefix="/api/inference", tags=["inference"])


MODEL_PATH =(
    "/home/intelliscan/Documents/intelliscan/models/"
    "gemma-4-E2B-it.litertlm"
)


camera_service = CameraService(
    output_dir="/home/intelliscan/Documents/intelliscan/data/captures",
    width=640,
    height=480,
)

gemma_service = GemmaService(
    MODEL_PATH,
    cpu_threads=4,
    visual_token_budget=70,
)




INSPECTION_PROMPT = """
        You are a strict food-crop inspection system.

        STEP 1 — IDENTIFY THE OBJECT

        The image must contain exactly one supported crop:

        Yam
        Orange

        If the main object is not clearly one of these crops, return UNKNOWN.

        If you are uncertain, return UNKNOWN.
        NEVER guess.

        A person, hand, face, animal, clothing, tool, table, phone,
        bottle, package, machine, room, or other object is UNKNOWN.

        For an unsupported image, return exactly:

        Crop: UNKNOWN
        Condition: UNKNOWN
        Defect: UNSUPPORTED IMAGE

        STEP 2 — INSPECT THE CROP

        Only if the object is Yam or Orange:

        Inspect the entire visible crop for clearly abnormal regions.

        Look for:
        mold, fuzzy growth, rot, decay, bruises, damaged skin,
        dark/black/brown/grey/green/white patches, spots,
        discoloration, cracks, holes, cuts, sunken areas,
        and abnormal texture.

        If exposed flesh is visible, inspect it for dark, brown,
        discolored, rotten, moldy, damaged, or abnormal tissue.

        Do not ignore a localized defect because the rest looks healthy.
        Do not call clearly abnormal discoloration normal variation.

        Use only visible evidence.
        Do not infer hidden damage.

        GOOD = no clearly visible abnormality.
        DEFECTIVE = at least one clearly visible abnormality.

        Return exactly three lines:

        Crop: <Yam|Orange|UNKNOWN>
        Condition: <GOOD|DEFECTIVE|UNKNOWN>
        Defect: <NONE|short visible description|UNSUPPORTED IMAGE>
""".strip()






VALID_CROPS = {
    "Yam",
    "Sweet Potato",
    "Orange",
    "UNKNOWN",
}

VALID_CONDITIONS = {
    "GOOD",
    "DEFECTIVE",
    "UNKNOWN",
}


def parse_inspection_response(response) ->dict:
    """Convert Gemma's text response into structured data."""

    text = response["content"][0]["text"]

    crop = "UNKNOWN"
    condition = "UNKNOWN"
    defect = "UNSUPPORTED IMAGE"

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("Crop:"):
            crop = line.split(":",1)[1].strip()

        elif line.startswith("Condition:"):
            condition = line.split(":", 1)[1].strip()

        elif line.startswith("Defect:"):
            defect = line.split(":", 1)[1].strip()

    
    # Backend validation.
    if crop not in VALID_CROPS:
        return {
            "crop": "UNKNOWN",
            "condition": "UNKNOWN",
            "defect": "UNSUPPORTED IMAGE",
        }

    if condition not in VALID_CONDITIONS:
        condition = "UNKNOWN"

    if condition == "UNKNOWN":
        defect = "UNSUPPORTED IMAGE"

    return {
        "crop": crop,
        "condition": condition,
        "defect": defect,
    }

@router.post("/capture")
def capture_camera():
    """Capture an image for inspection without running AI inference."""
    try:
        camera_service.start()

        image_path = camera_service.capture(
            "latest_inspection.jpg"
        )

        return {
            "image": str(image_path),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post("/inspect")
def inspect_camera():
    """Capture an image and inspect it wth Gemma 4."""

    try:
        camera_service.start()

        image_path= camera_service.capture(
            "latest_inspection.jpg"
        )

        result = gemma_service.inspect_image(
            image_path,
            INSPECTION_PROMPT,
            max_output_tokens =30
        )

        parsed = parse_inspection_response(result["response"])

        return {
            **parsed,
            "image": str(image_path),
            "elapsed_time": result["elapsed_time"],
            "visual_token_budget": result["visual_token_budget"],
        }

        # return {
        #     "image": str(image_path),
        #     "response": result["response"],
        #     "elapsed_time":result["elapsed_time"],
        #     "visual_token_budget": result["visual_token_budget"]

        # }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )from exc





    