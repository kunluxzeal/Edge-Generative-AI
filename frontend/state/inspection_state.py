import httpx 
import reflex as rx


BACKEND_URL = "http://127.0.0.1:8000"



class InspectionState(rx.State):
    # --------------------
    # Analysis state
    # --------------------

    analyzing: bool = False

    crop: str = "—"
    condition: str = "—"
    defect: str = "No inspection yet"

    inference_time: str = "—"
    visual_token_budget: str = "70"

    status: str = "READY"
    error_message: str = ""


    #Used to force the inspection image to refresh
    image_version: int = 0

    @rx.var
    def inspection_image_url(self) -> str:
        return(
            f"{BACKEND_URL}/api/camera/inspection"
            f"?v={self.image_version}"
        )



    @rx.event(background=True)
    async def analyze(self):

        # ==========================================
        # STEP 1 — Capture and immediately show image
        # ==========================================

        async with self:
            if self.analyzing:
                return

            self.analyzing = True
            self.status = "ANALYZING"
            self.error_message = ""

        try:

            async with httpx.AsyncClient(timeout=120.0) as client:

                # Capture image first
                capture_response = await client.post(
                    f"{BACKEND_URL}/api/inference/capture"
                )

                capture_response.raise_for_status()

            # Tell Reflex to reload the inspection image
            async with self:
                self.image_version += 1

            # ==========================================
            # STEP 2 — Now run Gemma inference
            # ==========================================

            async with httpx.AsyncClient(timeout=120.0) as client:

                response = await client.post(
                    f"{BACKEND_URL}/api/inference/inspect"
                )

                response.raise_for_status()

                data = response.json()

            # ==========================================
            # STEP 3 — Display AI result
            # ==========================================

            async with self:

                self.crop = data.get(
                    "crop",
                    "UNKNOWN",
                )

                self.condition = data.get(
                    "condition",
                    "UNKNOWN",
                )

                self.defect = data.get(
                    "defect",
                    "UNKNOWN",
                )

                elapsed = data.get("elapsed_time")

                if elapsed is not None:
                    self.inference_time = f"{elapsed:.2f} s"
                else:
                    self.inference_time = "—"

                budget = data.get(
                    "visual_token_budget"
                )

                if budget is not None:
                    self.visual_token_budget = str(budget)

                self.status = "COMPLETE"

        except httpx.HTTPStatusError as exc:

            async with self:
                self.status = "ERROR"

                self.error_message = (
                    f"Backend returned "
                    f"{exc.response.status_code}"
                )

        except Exception as exc:

            async with self:
                self.status = "ERROR"

                self.error_message = (
                    f"Analysis failed: {exc}"
                )

        finally:

            async with self:
                self.analyzing = False