from __future__ import annotations
import io 
from PIL import Image
import time 
from pathlib import Path
from picamera2 import Picamera2


class CameraService:
    def __init__(
        self,
        output_dir:str | Path="/tmp/intelliscan", 
        width:int =480, 
        height: int = 320,
    ):
        self.output_dir = Path(output_dir)
        self.width = width
        self.height = height 

        self.camera: Picamera2 | None=None
        self.started = False

    def start(self) -> None:
        """ Intitalize and start the camera."""
        if self.started:
            return
        
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.camera = Picamera2()

        config = self.camera.create_still_configuration(
            main={
                "size":(self.width,self.height),
                "format":"RGB888",
            }
        )

        self.camera.configure(config)
        self.camera.start()

        #Allow sensor auto-exposure and auto-white-balace to settlr
        time.sleep(1)


        self.started =True

    def capture(self, filename:str= "inspection.jpg") -> Path:
        """Capture one image and return its path."""
        if not self.started or self.camera is None:
            raise RuntimeError(
                "CameraService is  not started. call start() first."
            )
        
        output_path = self.output_dir / filename

        self.camera.capture_file(str(output_path))

        return output_path

    def capture_frame(self) -> bytes:
        """Capture one preview frame as JPEG bytes"""
        if not self.started or self.camera is None:
            raise RuntimeError(
                "cameraServise is not started. call start() first."
            )
        frame = self.camera.capture_array()

        # Picamera2 RGB888 numpy buffers are BGR ordered.
        frame = frame[:, :, ::-1]


        image = Image.fromarray(frame)

        buffer = io.BytesIO()

        image.save(
            buffer,
            format = "JPEG",
            quality = 80,

        )
        return buffer.getvalue()

    def generate_frames(self):
        """Generate continous JPEG frames for MJPEG streaming."""
        if not self.started or self.camera is None:
            raise RuntimeError("CameraService is not started.")

        while self.started:
            frame = self.camera.capture_array()

            #Picamera2 RGB888 numpy buffers are BGR ordered
            frame = frame[:, :,  ::-1]

            image = Image.fromarray(frame)

            buffer = io.BytesIO()

            image.save(
                buffer,
                format = "JPEG",
                quality = 80,
            )

            jpeg = buffer.getvalue()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Content-Length: "
                + str(len(jpeg)).encode()
                + b"\r\n"
                b"\r\n"
                + jpeg
                + b"\r\n"
            )


            time.sleep(0.03)



    


    def stop(self) -> None:
        """Stop the camera."""
        if self.camera is not None and self.started:
            if self.started:
                self.camera.stop()

        self.started =False

    def close(self) -> None:
        """Release camera resources."""
        if self.camera is not None:
            if self.started:
                self.camera.stop()

            self.camera.close()
            self.camera = None

        self.started = False




