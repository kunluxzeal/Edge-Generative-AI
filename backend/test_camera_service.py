from services.camera_service import CameraService

camera = CameraService(
    output_dir ="/home/intelliscan/Documents/intelliscan/test_images",
    width =164,
    height=148,
)

try:
    print("Starting camera...")
    camera.start()

    print("Capturing image...")
    image_path = camera.capture("camera_service_test.jpg")

    print(f"Caputred:{image_path}")

finally:
    camera.close()
    print("camera closed.")