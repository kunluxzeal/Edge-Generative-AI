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
    width=320,
    height=240,
)

gemma_service = GemmaService(
    MODEL_PATH,
    cpu_threads=4,
    visual_token_budget=70,
)


# INSPECTION_PROMPT = """
#     You are a STRICT food-crop quality inspector.

#     Examine the ENTIRE image carefully before making a decision.

#     Identify the crop:
#     Yam, Sweet Potato, or Orange.

#     Then inspect every visible part of the crop for ABNORMALITY.

#     IMPORTANT:
#     Do NOT classify a clearly abnormal region as normal simply because
#     the rest of the crop looks healthy.

#     Look specifically for localized regions that are visually different
#     from the surrounding healthy tissue.

#     EXTERNAL SURFACE:

#     Look for:

#     - fuzzy or hairy growth
#     - grey patches
#     - green patches
#     - white patches
#     - black patches
#     - brown patches
#     - mold-like growth
#     - dark spots
#     - black spots
#     - brown spots
#     - rotting areas
#     - bruises
#     - sunken areas
#     - damaged skin
#     - unusual discoloration
#     - cracks
#     - holes
#     - cuts
#     - decay
#     - abnormal texture

#     A localized region that is clearly different in colour, texture,
#     shape, or appearance from the surrounding healthy surface MUST be
#     reported as an abnormality.

#     Do NOT dismiss a clearly localized abnormal region as
#     "natural colour variation".

#     Pay particular attention to:

#     - isolated dark regions
#     - black regions
#     - grey regions
#     - brown regions
#     - green regions
#     - fuzzy regions
#     - sunken regions
#     - visibly degraded regions

#     If one clearly abnormal region is visible, the crop is DEFECTIVE.

#     INTERNAL TISSUE:

#     If the crop is cut, sliced, peeled, or broken and flesh is visible,
#     inspect the exposed flesh separately.

#     Look for:

#     - black tissue
#     - dark brown tissue
#     - brown discoloration
#     - abnormal colour
#     - rot
#     - mold
#     - decay
#     - damaged tissue
#     - cavities
#     - unusual texture
#     - degraded tissue

#     If internal tissue cannot be seen, write:

#     Internal: NOT VISIBLE

#     IMPORTANT DECISION RULE:

#     GOOD =
#     No clearly visible abnormal region exists.

#     DEFECTIVE =
#     At least ONE clearly visible abnormal region exists on either:

#     1. the external surface
#     OR
#     2. exposed internal tissue.

#     Do NOT require the entire crop to look damaged.

#     A single clearly visible defect is sufficient for DEFECTIVE.

#     Use ONLY visible evidence.

#     Do not infer hidden damage.

#     Return ONLY these three lines:

#     Crop: <Yam|Sweet Potato|Orange>
#     Condition: <GOOD|DEFECTIVE>
#     Defect: <NONE|short description>

# """.strip()


INSPECTION_PROMPT = """
        You are a strict food-crop inspection system.

        STEP 1 — IDENTIFY THE OBJECT

        The image must contain exactly one supported crop:

        Yam
        Sweet Potato
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

        Only if the object is Yam, Sweet Potato, or Orange:

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

        Crop: <Yam|Sweet Potato|Orange|UNKNOWN>
        Condition: <GOOD|DEFECTIVE|UNKNOWN>
        Defect: <NONE|short visible description|UNSUPPORTED IMAGE>
""".strip()


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

        return {
            "image": str(image_path),
            "response": result["response"],
            "elapsed_time":result["elapsed_time"],
            "visual_token_budget": result["visual_token_budget"]

        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )from exc
