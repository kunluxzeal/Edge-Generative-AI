# from services.gemma_service import GemmaService


# MODEL_PATH = (
#     "/home/intelliscan/Documents/intelliscan/models/gemma-4-E2B-it.litertlm"
# )

# service = GemmaService(
#     model_path=MODEL_PATH,
#     cpu_threads=4,
# )


# try:
#     print("Loading Gemma 4...")
#     load_time = service.load()

#     print(f"Model loaded in {load_time:.3f} seconds")

#     print("\nSending prompt...")

#     result = service.generate("what is the capital of Nigeria?")


#     print("\n--- RESPONSE---")
#     print(result["response"])

#     print("\n ---METRICS ---")
#     print(f"Inference time: {result['elapsed_time']:.3f} seconds")

# finally:
#     service.close()
#     print("\nGemmaService closed.")


from services.gemma_service import GemmaService


MODEL_PATH = (
    "/home/intelliscan/Documents/intelliscan/models/"
    "gemma-4-E2B-it.litertlm"
)

IMAGE_PATH = (
    "/home/intelliscan/Documents/intelliscan/test_images/"
    "bad_yam.jpg"
)


service = GemmaService(
    MODEL_PATH,
    cpu_threads=4,
    visual_token_budget=70,
)

load_time = service.load()

print(f"Model loaded in {load_time:.3f} seconds")

prompt = """
    You are a STRICT food-crop quality inspector.

    Examine the ENTIRE image carefully before making a decision.

    Identify the crop:
    Yam, Sweet Potato, or Orange.

    Then inspect every visible part of the crop for ABNORMALITY.

    IMPORTANT:
    Do NOT classify a clearly abnormal region as normal simply because
    the rest of the crop looks healthy.

    Look specifically for localized regions that are visually different
    from the surrounding healthy tissue.

    EXTERNAL SURFACE:

    Look for:

    - fuzzy or hairy growth
    - grey patches
    - green patches
    - white patches
    - black patches
    - brown patches
    - mold-like growth
    - dark spots
    - black spots
    - brown spots
    - rotting areas
    - bruises
    - sunken areas
    - damaged skin
    - unusual discoloration
    - cracks
    - holes
    - cuts
    - decay
    - abnormal texture

    A localized region that is clearly different in colour, texture,
    shape, or appearance from the surrounding healthy surface MUST be
    reported as an abnormality.

    Do NOT dismiss a clearly localized abnormal region as
    "natural colour variation".

    Pay particular attention to:

    - isolated dark regions
    - black regions
    - grey regions
    - brown regions
    - green regions
    - fuzzy regions
    - sunken regions
    - visibly degraded regions

    If one clearly abnormal region is visible, the crop is DEFECTIVE.

    INTERNAL TISSUE:

    If the crop is cut, sliced, peeled, or broken and flesh is visible,
    inspect the exposed flesh separately.

    Look for:

    - black tissue
    - dark brown tissue
    - brown discoloration
    - abnormal colour
    - rot
    - mold
    - decay
    - damaged tissue
    - cavities
    - unusual texture
    - degraded tissue

    If internal tissue cannot be seen, write:

    Internal: NOT VISIBLE

    IMPORTANT DECISION RULE:

    GOOD =
    No clearly visible abnormal region exists.

    DEFECTIVE =
    At least ONE clearly visible abnormal region exists on either:

    1. the external surface
    OR
    2. exposed internal tissue.

    Do NOT require the entire crop to look damaged.

    A single clearly visible defect is sufficient for DEFECTIVE.

    Use ONLY visible evidence.

    Do not infer hidden damage.

    Return ONLY these three lines:

    Crop: <Yam|Sweet Potato|Orange>
    Condition: <GOOD|DEFECTIVE>
    Defect: <NONE|short description>

""".strip()

result = service.inspect_image(
    IMAGE_PATH,
    prompt,
    max_output_tokens=25,
)

print("\n--- RESPONSE ---")
print(result["response"])

print("\n--- METRICS ---")
print(f"Visual token budget: {result['visual_token_budget']}")
print(f"Inference time: {result['elapsed_time']:.3f} seconds")

service.close()