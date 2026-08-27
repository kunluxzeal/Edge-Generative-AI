from __future__ import annotations

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




