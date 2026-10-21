IntelliScan — Offline Multimodal Edge AI Crop Inspection
IntelliScan is an edge-AI crop inspection application built around a Raspberry Pi 5, an IMX477 camera, Gemma 4 E2B, LiteRT-LM, FastAPI, and a Reflex frontend. It is designed to inspect supported crops locally and return a concise quality assessment without sending images to a cloud inference service.

The supported crop classes are:
- Yam
- Sweet Potato
- Orange
Images that do not contain a supported crop should be returned as UNKNOWN with the condition UNKNOWN and defect UNSUPPORTED IMAGE.
Project status: The camera has been detected and tested through the Raspberry Pi camera stack and Picamera2. The FastAPI camera endpoints and one-shot Gemma inference endpoint have been tested. The Reflex frontend contains Home, Inspection, and Settings pages. Any frontend action or settings control should be considered fully operational only after it has been connected to and tested against the backend.

Contents
- Features
- System architecture
- Hardware and software requirements
- Repository structure
- Installation
- Configure the application
- Run IntelliScan
- Backend API
- Inspection response
- Testing
- Troubleshooting
- Operational notes
- Roadmap
Features
- On-device vision inference: Gemma 4 E2B is loaded locally through LiteRT-LM and the CPU backend.
- Raspberry Pi camera integration: Captures images from the IMX477 using Picamera2 and the system libcamera stack.
- Live preview: An MJPEG endpoint provides a continuously updating browser preview.
- Inspection capture: Saves the most recent inspection image so the frontend can show the same frame that was submitted for inference.
- Crop quality assessment: The model is prompted to inspect for visible mold, fuzzy growth, rot, decay, bruising, localized discoloration, damaged skin, spots, and abnormal texture.
- Unsupported-image handling: The application normalizes unsupported crop/object results to UNKNOWN where the backend response parser is applied.
- Structured API output: The inference route returns crop, condition, defect description, image path, elapsed inference time, and visual-token budget.
- Reflex UI: The frontend is organized into Home, Inspection, and Settings pages.
System architecture
IMX477 camera
    |
    v
Raspberry Pi camera stack (libcamera / RP1 CSI / PiSP)
    |
    v
Picamera2
    |
    v
CameraService ----------------------> /api/camera/stream (MJPEG)
    |                                /api/camera/frame (JPEG)
    |
    +--> data/captures/latest_inspection.jpg
                 |
                 v
          GemmaService
          LiteRT-LM / Gemma 4 E2B
                 |
                 v
         Parse and validate result
                 |
                 v
          FastAPI JSON response
                 |
                 v
           Reflex frontend
The camera preview and AI inspection are separate operations. The camera can keep streaming while Gemma processes a single captured image. Gemma inference currently takes several seconds per image, so running inference on every camera frame is not recommended.
Hardware and software requirements
Hardware
- Raspberry Pi 5 (the current development target)
- Raspberry Pi HQ Camera / compatible IMX477 camera module
- Compatible CSI ribbon cable connected to a Pi 5 camera connector
- Raspberry Pi power supply suitable for the board and attached hardware
- Display and browser for kiosk use, or another computer on the same network for development
Software
The current development environment has been tested with the following general stack:
- Raspberry Pi OS, 64-bit, Debian 13-based
- Python 3.13
- uv for Python dependency and environment management
- python3-libcamera and the Raspberry Pi camera utilities from the OS packages
- Picamera2
- LiteRT-LM 0.16.1
- FastAPI and Uvicorn
- Reflex 0.9.8.post1
Exact package versions can differ as Raspberry Pi OS and Python packages evolve. The native libcamera Python binding should come from the Raspberry Pi OS packages and must be visible to the backend virtual environment.
Repository structure
intelliscan/
├── backend/
│   ├── api/
│   │   ├── camera.py             # Camera frame, stream, and inspection-image routes
│   │   ├── health.py             # Health-related routes (if registered)
│   │   ├── inference.py          # Gemma inspection API and prompt
│   │   └── system.py             # System-related routes (if registered)
│   ├── config/
│   │   └── settings.py           # Backend configuration
│   ├── models/
│   │   └── schemas.py            # Request/response models
│   ├── services/
│   │   ├── camera_service.py     # Picamera2 lifecycle, capture, and frames
│   │   ├── gemma_service.py      # LiteRT-LM engine and image inference
│   │   └── metrics_service.py    # Timing/performance helpers
│   ├── main.py                   # FastAPI application and service lifecycle
│   ├── test_camera_service.py
│   ├── test_gemma_budget.py
│   ├── test_gemma_service.py
│   ├── test_gemma_vision.py
│   ├── pyproject.toml
│   └── uv.lock
├── data/
│   ├── captures/                 # Most recent inspection image
│   └── logs/                     # Intended application-log directory
├── frontend/
│   ├── assets/                   # Images/icons served by Reflex
│   ├── pages/
│   │   ├── home.py               # Home page
│   │   ├── inspection.py         # Camera and inspection UI
│   │   └── settings.py           # Settings UI
│   ├── state/
│   │   └── inspection_state.py   # Reflex inspection state/events
│   ├── main.py                   # Reflex app and page routes
│   ├── rxconfig.py               # Reflex configuration
│   ├── pyproject.toml
│   └── uv.lock
├── models/
│   └── gemma-4-E2B-it.litertlm   # Local Gemma 4 E2B model directory
├── scripts/                     # Utility scripts
├── test_images/                  # Manual/test images
├── tests/
│   ├── backend/
│   └── frontend/
├── LICENSE
└── README.md
Python __pycache__ folders and compiled .pyc files are generated automatically and are not source files.
Installation
1. Install Raspberry Pi camera system packages
On the Raspberry Pi, install the camera stack and build dependency used by python-prctl:
sudo apt update
sudo apt install -y \
  python3-libcamera \
  python3-picamera2 \
  libcamera-tools \
  rpicam-apps \
  libcap-dev
If you need I²C diagnostics while troubleshooting the camera, install i2c-tools as well:
sudo apt install -y i2c-tools
2. Check the IMX477 camera
Before debugging Python, confirm that the OS sees the camera:
rpicam-hello --list-cameras
A successful result should list an IMX477 camera. To test a still capture:
mkdir -p ~/Documents/intelliscan/test_images
rpicam-still \
  -o ~/Documents/intelliscan/test_images/camera_test.jpg \
  --width 320 \
  --height 240 \
  --nopreview
If rpicam-hello reports No cameras available, troubleshoot the CSI cable, connector orientation, camera overlay, and sensor detection before changing the Python application.
3. Set up the backend environment
cd ~/Documents/intelliscan/backend
The backend needs access to the OS-provided libcamera Python module. If you are creating the virtual environment for the first time, create it with system site packages enabled:
uv venv .venv --system-site-packages
uv sync
Important: Do not recreate this environment with a plain uv venv .venv unless you also re-enable system site packages. Otherwise picamera2 may be installed in the virtual environment but fail with ModuleNotFoundError: No module named 'libcamera'.

Verify the core imports:
uv run python - <<'PY'
import litert_lm
import libcamera
from picamera2 import Picamera2

print("LiteRT-LM: OK")
print("libcamera:", libcamera.__file__)
print("Picamera2: OK")
PY
4. Set up the Reflex frontend environment
cd ~/Documents/intelliscan/frontend
uv sync
uv run reflex --version
The project uses rxconfig.py and main.py. Keep the app_name and app-module configuration consistent with the actual Reflex entry point in this repository.
Configure the application
Model path
The inference module currently uses a model path similar to:
/home/intelliscan/Documents/intelliscan/models/gemma-4-E2B-it.litertlm
If the repository is moved to another directory or username, update the model path in backend/api/inference.py or centralize it in backend/config/settings.py.

The model is a directory, not necessarily one standalone file. LiteRT-LM may create adjacent cache files during model initialization. Keep the model files and their generated caches on storage with enough free space.
Camera capture directory
Inspection images are saved under:
/home/intelliscan/Documents/intelliscan/data/captures/
The current API uses latest_inspection.jpg for the most recent inspection. A new inspection overwrites that image. Unique per-inspection filenames and a history page are planned improvements, not part of the current latest-image workflow.
Vision settings
The current inspected configuration has used:
- CPU threads: 4
- visual-token budget: 70
- inspection image size: 320 × 240
- output token budget: commonly 48
These values are configured in the backend service/API code. Do not assume that dropdowns shown on the Settings page change the running backend until those controls have been explicitly wired to Reflex state and a backend configuration endpoint.
Backend URL in the frontend
The Inspection page currently references the backend with a value similar to:
BACKEND_URL = "http://127.0.0.1:8000"
This is correct when the browser is running on the Raspberry Pi itself. If the Reflex frontend is opened from another computer, 127.0.0.1 points to that computer, not the Pi. In that case, use the Raspberry Pi's LAN address, for example:
BACKEND_URL = "http://192.168.1.50:8000"
Replace the example address with the real address of the Raspberry Pi. For a more portable deployment, move the backend base URL to a frontend configuration/environment variable.
Run IntelliScan
Run the backend and frontend in separate terminal sessions. Start the backend first so the API is available to the UI.
Terminal 1 — FastAPI backend
cd ~/Documents/intelliscan/backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000
The FastAPI application loads Gemma and starts the camera through its application lifecycle. Model initialization can take time. Keep a single Uvicorn worker for this setup because the application owns one camera and one loaded Gemma engine; multiple worker processes could try to acquire the camera and duplicate model memory.

Useful backend URLs:
- API root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs
Terminal 2 — Reflex frontend
cd ~/Documents/intelliscan/frontend
uv run reflex run
Open the frontend URL reported by Reflex. It is commonly:
http://127.0.0.1:3000
The Reflex development backend may choose port 8001 when port 8000 is already occupied by FastAPI. That is expected: the FastAPI backend remains on 8000, and the Reflex frontend is normally served on 3000.
Main navigation
The intended frontend pages are:
Route	Purpose
/	Home / start screen
/inspection	Live preview, captured inspection image, and result summary
/settings	Camera, AI, and system settings UI


Backend API
The following endpoints have been used or tested during development. The interactive /docs page is the source of truth for the currently registered routes.
Method	Endpoint	Purpose	Expected result
GET	/	API root/status	JSON service message
GET	/health	Basic health status	JSON health response
GET	/api/test	Simple test route	JSON test response
GET	/api/camera/frame	Return one JPEG frame	image/jpeg
GET	/api/camera/stream	Live MJPEG stream	multipart/x-mixed-replace
GET	/api/camera/inspection	Return latest inspection JPEG	image/jpeg, or 404 before one exists
POST	/api/inference/inspect	Capture an image and run Gemma inspection	Structured JSON result


Test a single frame
curl -f http://127.0.0.1:8000/api/camera/frame \
  --output /tmp/iscan-frame.jpg
file /tmp/iscan-frame.jpg
View the live stream
Open this URL in a browser:
http://127.0.0.1:8000/api/camera/stream
The stream should remain open and show continuously updating images. An MJPEG stream is not a normal one-off JPEG response; every frame must include the multipart boundary and Content-Type: image/jpeg headers.
View the most recent inspection image
http://127.0.0.1:8000/api/camera/inspection
This displays the last image written to data/captures/latest_inspection.jpg. It will not automatically represent a new inspection until /api/inference/inspect has captured another image.
Trigger inspection in Postman or curl
Use POST with no request body:
curl -X POST http://127.0.0.1:8000/api/inference/inspect
The endpoint captures an image from the camera, sends that image and the configured inspection prompt to Gemma, parses the response, and returns JSON. No image upload is needed for this camera-driven endpoint.
Inspection response
A supported crop result has this general shape:
{
  "crop": "Orange",
  "condition": "DEFECTIVE",
  "defect": "Dark surface rot",
  "image": "/home/intelliscan/Documents/intelliscan/data/captures/latest_inspection.jpg",
  "elapsed_time": 9.33,
  "visual_token_budget": 70
}
The values above are illustrative; actual text and timing depend on the captured image and inference run.

For an unsupported object, the intended normalized result is:
{
  "crop": "UNKNOWN",
  "condition": "UNKNOWN",
  "defect": "UNSUPPORTED IMAGE",
  "image": "/home/intelliscan/Documents/intelliscan/data/captures/latest_inspection.jpg",
  "elapsed_time": 8.81,
  "visual_token_budget": 70
}
The supported output vocabulary is:
- crop: Yam, Sweet Potato, Orange, or UNKNOWN
- condition: GOOD, DEFECTIVE, or UNKNOWN
- defect: NONE, a short visible defect description, or UNSUPPORTED IMAGE
The model should only report visible evidence. It cannot determine internal damage when the crop's flesh is not visible. Results are AI-assisted visual assessments and should not be treated as a guarantee of food safety.
Testing
Camera hardware / Picamera2
cd ~/Documents/intelliscan/backend
uv run python -c "from picamera2 import Picamera2; print('Picamera2 OK')"
uv run python test_camera_service.py
Confirm the capture file exists in the configured test/capture directory and is a valid JPEG.
Gemma vision
The repository includes focused scripts for service and vision-budget experiments:
cd ~/Documents/intelliscan/backend
uv run python test_gemma_service.py
uv run python test_gemma_vision.py
uv run python test_gemma_budget.py
Run each script only if its paths and inputs match the current device. Some scripts may be experiments rather than automated unit tests.
Frontend
Start Reflex and visit /, /inspection, and /settings. Verify navigation, image rendering, and the browser's network requests. Ensure the backend address used by the browser is correct for the device/network where the browser is running.
Troubleshooting
No cameras available!
1. Check the physical CSI ribbon at both ends, with the Raspberry Pi powered off before reseating it.
2. Verify the cable is oriented correctly and the connector latches are secure.
3. Check the camera connector used on the Pi 5 and configure the matching camera overlay if manual configuration is required.
4. Inspect the kernel log:
   dmesg | grep -Ei 'imx477|rp1-cfe|csi|i2c|camera'
A log such as failed to read chip id 477 with error -121 indicates the sensor probe cannot communicate correctly over I²C. This is below Python/FastAPI and usually requires checking the cable, connector, port configuration, or camera module.
Picamera2 import works in system Python but not in uv run
The virtual environment needs access to the OS libcamera binding. Recreate it only if necessary, with system site packages enabled:
cd ~/Documents/intelliscan/backend
uv venv .venv --system-site-packages
uv sync
Then verify:
uv run python -c "import libcamera; from picamera2 import Picamera2; print('camera imports OK')"
Blue/pink or otherwise incorrect preview colours
Picamera2's RGB888 stream can have BGR byte ordering in the returned array. If the preview image is built manually with Pillow, confirm that the channel order is corrected consistently before JPEG encoding. Avoid swapping channels twice or applying one channel order to preview and another to inspection unintentionally.
/api/camera/stream keeps loading but shows no image
Check that the endpoint returns multipart/x-mixed-replace; boundary=frame and each frame includes the correct boundary, Content-Type: image/jpeg, a blank line, the JPEG bytes, and a trailing CRLF. Confirm /api/camera/frame returns a valid JPEG first.
ModuleNotFoundError: No module named 'libcamera'
Install the OS package (python3-libcamera) and make the backend virtual environment see system site packages. Do not try to replace the Raspberry Pi OS camera binding with an unrelated PyPI package.
GemmaService is not loaded
The Gemma engine must be loaded during FastAPI application startup before the inference endpoint is called. Do not load the full model for every request.
litert_lm_conversation_send_message failed / Task failed with state: 7
The image preprocessor may have successfully resized the image even though inference then fails. Check the complete exception/log, memory availability, and whether repeated calls are reusing conversation state incorrectly. The current service's vision path uses a fresh conversation per inspection to avoid long-lived vision-session state accumulating. Keep requests sequential while debugging.
Postman returns 404 Not Found
Use the full path:
POST http://127.0.0.1:8000/api/inference/inspect
POST /inspect and POST / are different paths and will not call this route.
Browser displays an error for /api/camera/inspection
The endpoint returns the most recent captured image. Trigger an inspection first so data/captures/latest_inspection.jpg exists, and check that the configured path matches the real project directory.
Reflex cannot find rxconfig.py or the app module
Run uv run reflex run from the frontend project root:
cd ~/Documents/intelliscan/frontend
uv run reflex run
Ensure rxconfig.py uses an app_name/module configuration compatible with the current main.py entry point and the installed Reflex version. If Reflex reports Module ... not found, inspect rxconfig.py and main.py together rather than randomly renaming the project directory.
Reflex says port 8000 is already in use
FastAPI owns port 8000. Reflex may choose another backend port, such as 8001, for its development server. Keep the FastAPI API on 8000 unless you intentionally change both the backend port and the frontend's BACKEND_URL.
Operational notes
- Run one Uvicorn worker. A single process owns the camera and Gemma engine.
- Do not run inference on every preview frame. Capture a single frame when the operator requests an inspection.
- Serialize inference requests. The Raspberry Pi is a resource-constrained CPU device; concurrent inference requests can increase latency and risk runtime errors.
- Use a stable image for each inference. Save the camera image first and send that exact path to Gemma. The /api/camera/inspection endpoint should expose that same saved image.
- Treat the inspection image as temporary/latest-only. Each run overwrites latest_inspection.jpg in the current design.
- Do not commit model weights or generated cache files to source control. The model directory is large and model redistribution must follow the applicable Gemma terms.
- Avoid exposing the development API to untrusted networks. The current endpoints are designed for a local device/LAN and do not provide authentication by default.
- Settings are not necessarily live configuration. UI dropdowns must be connected to Reflex state and validated backend configuration before they change the running camera or model.
- Keep camera colour handling consistent. Defect recognition can be affected if blue, green, brown, or orange hues are transformed during preview/capture.
Roadmap
The following are natural next steps for the project; they should be marked complete only after implementation and testing:
1. Finish Reflex integration: wire the Analyze button to POST /api/inference/inspect, display loading/processing states, and refresh the frozen inspection image when inference completes.
2. Keep the page viewport-sized: tune the Inspection page for the target display while retaining sensible behavior on smaller screens.
3. Live service status: populate camera, backend, and model status from actual health endpoints instead of static labels.
4. Functional Settings: persist preview resolution and inference settings, validate supported values, and apply them safely to the backend.
5. Inspection history: save unique filenames and an inspection ID instead of overwriting only latest_inspection.jpg.
6. Structured validation/tests: strengthen parsing for malformed or truncated Gemma output and add repeatable tests for supported crops, rotten crops, healthy crops, and unsupported objects.
7. Performance tracking: record capture time, inference time, and end-to-end request time in data/logs/.
8. Deployment hardening: configure startup services, environment-based paths/URLs, and appropriate network access controls.
License and model terms
This repository contains application code and may reference a separately stored Gemma model. Review the repository's LICENSE for the application's code and comply with the applicable Gemma model terms for the model weights and any distribution. Do not assume that the code license also grants unrestricted redistribution rights for the model.
Acknowledgements
IntelliScan builds on the Raspberry Pi camera stack, Picamera2, FastAPI, Reflex, LiteRT-LM, and Google's Gemma model family.