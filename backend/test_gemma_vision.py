import time
from PIL import Image
import litert_lm


MODEL_PATH = "/home/intelliscan/Documents/intelliscan/models/gemma-4-E2B-it.litertlm"
IMAGE_PATH = "/home/intelliscan/Documents/intelliscan/test_images/bad_yam.jpg"
RESIZED_IMAGE_PATH = "/tmp/gemma_test_320x180.jpg"


print("=" * 60)
print("Gemma 4 Vision Performance Test")
print("=" * 60)


# ---------------------------------------------------------
# 1. Load model
# ---------------------------------------------------------

print("\n[1] Loading Gemma 4...")

cpu_backend = litert_lm.interfaces.CPU(thread_count=3)

start = time.perf_counter()

engine = litert_lm.Engine(
    MODEL_PATH,
    backend=cpu_backend,
    vision_backend=cpu_backend,
    max_num_images=1,
)

load_time = time.perf_counter() - start

print(f"Model loaded in: {load_time:.3f} seconds")


# ---------------------------------------------------------
# 2. Load image
# ---------------------------------------------------------

print("\n[2] Loading image...")

start = time.perf_counter()

image = Image.open(IMAGE_PATH)

image_load_time = time.perf_counter() - start

print(f"Original image size: {image.size}")
print(f"Image load time: {image_load_time:.3f} seconds")


# ---------------------------------------------------------
# 3. Resize image
# ---------------------------------------------------------

print("\n[3] Resizing image...")

start = time.perf_counter()

image = image.resize((320, 180))

image.save(
    RESIZED_IMAGE_PATH,
    "JPEG",
    quality=85,
)

resize_time = time.perf_counter() - start

print(f"Resized image: {image.size}")
print(f"Resize/save time: {resize_time:.3f} seconds")


# ---------------------------------------------------------
# 4. Create conversation
# ---------------------------------------------------------

print("\n[4] Creating conversation...")

start = time.perf_counter()

conversation = engine.create_conversation()

conversation_time = time.perf_counter() - start

print(f"Conversation creation: {conversation_time:.3f} seconds")


# ---------------------------------------------------------
# 5. Prepare image content
# ---------------------------------------------------------

print("\n[5] Preparing image content...")

start = time.perf_counter()

image_content = litert_lm.Content.ImageFile(
    RESIZED_IMAGE_PATH
)

image_prepare_time = time.perf_counter() - start

print(f"Image content preparation: {image_prepare_time:.3f} seconds")


# ---------------------------------------------------------
# 6. Prepare prompt
# ---------------------------------------------------------

print("\n[6] Preparing prompt...")

start = time.perf_counter()

prompt = """You are a strict food-crop quality inspector.

Identify: Yam, Sweet Potato, or Orange.

Inspect the entire visible crop for abnormal regions.

Check the outside for discoloration, dark/black/brown/grey/green/white patches, mold, fuzzy growth, rot, bruises, holes, cuts, cracks, sunken areas, or abnormal texture.

If flesh is exposed, inspect it for dark/black/brown tissue, discoloration, rot, mold, decay, cavities, or abnormal texture.

ONE clearly visible defect = DEFECTIVE.
No visible defect = GOOD.
Use only visible evidence.

IMPORTANT:
If exposed flesh is visible, describe the defect under Internal, NOT External.
If exposed flesh is not visible, use Internal: NOT VISIBLE.

Return ONLY these 5 lines:

Crop: <Yam|Sweet Potato|Orange>
External: <NONE|short description>
Internal: <NONE|NOT VISIBLE|short description>
Condition: <GOOD|DEFECTIVE>
Defect: <NONE|short description>""".strip()

text = litert_lm.Content.Text(prompt)

contents = litert_lm.Contents([
    image_content,
    text,
])

message = litert_lm.Message.user(contents)

prompt_prepare_time = time.perf_counter() - start

print(f"Prompt preparation: {prompt_prepare_time:.3f} seconds")


# ---------------------------------------------------------
# 7. ACTUAL VISION + GENERATION
# ---------------------------------------------------------

print("\n[7] Running Gemma vision inference...")
print("This is the important measurement.")

start = time.perf_counter()

response = conversation.send_message(message)

inference_time = time.perf_counter() - start


# ---------------------------------------------------------
# 8. Results
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("RESPONSE")
print("=" * 60)

print(response)


print("\n" + "=" * 60)
print("PERFORMANCE")
print("=" * 60)

print(f"Model loading:          {load_time:.3f} s")
print(f"Image loading:          {image_load_time:.3f} s")
print(f"Image resize/save:      {resize_time:.3f} s")
print(f"Conversation creation:  {conversation_time:.3f} s")
print(f"Image preparation:      {image_prepare_time:.3f} s")
print(f"Prompt preparation:     {prompt_prepare_time:.3f} s")
print("-" * 60)
print(f"VISION + GENERATION:    {inference_time:.3f} s")


# ---------------------------------------------------------
# 9. Cleanup
# ---------------------------------------------------------

conversation.close()
engine.close()

print("\nGemma 4 vision test complete.")