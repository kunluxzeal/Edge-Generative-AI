# import time
# from pathlib import Path

# import litert_lm

# class GemmaService:
#     """ service responsible for Gemma 4 inference through LiteRT-LM."""
#     def __init__(self, model_path:str | Path, cpu_threads:int =4):
        
#         self.model_path = Path(model_path)
#         self.cpu_threads = cpu_threads

#         self.engine = None
#         self.conversation = None

#     def load(self) -> float:
#         """ Load the Gemma model and create a conversation 
        
#         Returns:
#         Model initialization time in seconds.

#         """
#         if not self.model_path.exists():
#             raise FileNotFoundError(
#                 f"Gemma model not found: {self.model_path}"
#             )
        
#         start = time.perf_counter()

#         self.engine = litert_lm.Engine(
#             str(self.model_path),
#             backend=litert_lm.Backend.CPU(
#                 thread_count=self.cpu_threads
#             ),
#         )

#         self.conversation = self.engine.create_conversation()

#         elapsed = time.perf_counter() - start

#         return elapsed

#     def generate(self, prompt:str, max_output_tokens: int | None = None) -> dict:
        
#         """Generate a text response from Gemma.

#         Args:
#             prompt: User prompt
#             max_output_tokens: Optional generation limit

#         Returns:
#             Dictionary containing the model response and timing.
#         """

#         if self.conversation is None:
#             raise RuntimeError("GemmaService is not loaded. Call load() first ")

#         if not prompt.strip():
#             raise ValueError("Prompt cannot be empty.")

#         start = time.perf_counter()

#         response = self.conversation.send_message(
#             prompt, 
#             max_output_tokens=max_output_tokens,
#         )

#         elapsed = time.perf_counter() - start

#         return {
#             "response": response,
#             "elapsed_time": elapsed,
#         }

#     def close(self) -> None:
#             """Release LiteRT-LM resources."""
#             if self.conversation is not None:
#                 self.conversation.close()
#                 self.conversation = None

#             if self.engine is not None:
#                 self.engine.close()
#                 self.engine = None


import ctypes
import time
from pathlib import Path

import litert_lm


class GemmaService:
    """Gemma 4 inference service using LiteRT-LM."""

    def __init__(
        self,
        model_path: str | Path,
        cpu_threads: int = 4,
        visual_token_budget: int = 70,
    ):
        self.model_path = Path(model_path)
        self.cpu_threads = cpu_threads
        self.visual_token_budget = visual_token_budget

        self.engine = None
        self.conversation = None

    def load(self) -> float:
        """Load the Gemma model and create a conversation."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Gemma model not found: {self.model_path}"
            )

        start = time.perf_counter()

        cpu_backend = litert_lm.interfaces.CPU(
            thread_count=self.cpu_threads
        )

        self.engine = litert_lm.Engine(
            str(self.model_path),
            backend=cpu_backend,
            vision_backend=cpu_backend,
            max_num_images=1,
        )

        self.conversation = self.engine.create_conversation()

        return time.perf_counter() - start

    def generate(
        self,
        prompt: str,
        max_output_tokens: int | None = None,
    ) -> dict:
        """Generate a text-only response."""
        if self.conversation is None:
            raise RuntimeError(
                "GemmaService is not loaded. Call load() first."
            )

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        start = time.perf_counter()

        response = self.conversation.send_message(
            prompt,
            max_output_tokens=max_output_tokens,
        )

        elapsed = time.perf_counter() - start

        return {
            "response": response,
            "elapsed_time": elapsed,
        }

    # def inspect_image(
    #     self,
    #     image_path: str | Path,
    #     prompt: str,
    #     max_output_tokens: int | None = 48,
    # ) -> dict:
    #     """Inspect an image using Gemma 4 vision."""

    #     if self.conversation is None:
    #         raise RuntimeError(
    #             "GemmaService is not loaded. Call load() first."
    #         )

    #     image_path = Path(image_path)

    #     if not image_path.exists():
    #         raise FileNotFoundError(
    #             f"Image not found: {image_path}"
    #         )

    #     if not prompt.strip():
    #         raise ValueError("Prompt cannot be empty.")


    #     # Create a fresh conversation for this viion request.
    #     conversation = self.engine.create_conversation()

    #     lib = self.conversation._lib

    #     # LiteRT-LM 0.16.1 exposes this native function,
    #     # but the Python wrapper does not expose it.
    #     lib.litert_lm_conversation_optional_args_create.restype = (
    #         ctypes.c_void_p
    #     )

    #     lib.litert_lm_conversation_optional_args_create.argtypes = []

    #     lib.litert_lm_conversation_optional_args_set_visual_token_budget.argtypes = [
    #         ctypes.c_void_p,
    #         ctypes.c_int,
    #     ]

    #     # Save LiteRT-LM's normal optional-argument creator.
    #     original_create = self.conversation._create_optional_args

    #     def custom_create(*args, **kwargs):
    #         # Let LiteRT-LM create the pointer normally.
    #         ptr = original_create(*args, **kwargs)

    #         # Some calls do not need optional arguments.
    #         # We still need a pointer because we want to set
    #         # the visual token budget.
    #         if ptr is None:
    #             ptr = (
    #                 lib.litert_lm_conversation_optional_args_create()
    #             )

    #             if not ptr:
    #                 raise RuntimeError(
    #                     "Failed to create LiteRT-LM optional arguments."
    #                 )

    #         # Add our visual token budget to this SAME pointer.
    #         lib.litert_lm_conversation_optional_args_set_visual_token_budget(
    #             ptr,
    #             self.visual_token_budget,
    #         )

    #         return ptr

    #     self.conversation._create_optional_args = custom_create

    #     try:
    #         message = litert_lm.Message.user(
    #             litert_lm.Contents(
    #                 [
    #                     litert_lm.Content.ImageFile(
    #                         str(image_path)
    #                     ),
    #                     litert_lm.Content.Text(
    #                         prompt
    #                     ),
    #                 ]
    #             )
    #         )

    #         start = time.perf_counter()

    #         response = self.conversation.send_message(
    #             message,
    #             max_output_tokens=max_output_tokens,
    #             thinking_config=litert_lm.ThinkingConfig(
    #                 enable_thinking=False,
    #                 thinking_token_budget=0,
    #             ),
    #         )

    #         elapsed = time.perf_counter() - start

    #         return {
    #             "response": response,
    #             "elapsed_time": elapsed,
    #             "visual_token_budget": self.visual_token_budget,
    #         }

    #     finally:
    #         # Restore normal LiteRT-LM behavior.
    #         self.conversation._create_optional_args = original_create


    def inspect_image(
    self,
    image_path: str | Path,
    prompt: str,
    max_output_tokens: int | None = 48,
    ) -> dict:
        """Inspect one image using a fresh Gemma conversation."""

        if self.engine is None:
            raise RuntimeError(
                "GemmaService is not loaded. Call load() first."
            )

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # Create a fresh conversation for this vision request.
        conversation = self.engine.create_conversation()

        try:
            lib = conversation._lib

            # Native LiteRT-LM 0.16.1 API.
            lib.litert_lm_conversation_optional_args_create.restype = (
                ctypes.c_void_p
            )

            lib.litert_lm_conversation_optional_args_create.argtypes = []

            lib.litert_lm_conversation_optional_args_set_visual_token_budget.argtypes = [
                ctypes.c_void_p,
                ctypes.c_int,
            ]

            # Keep LiteRT-LM's normal optional-argument creation.
            original_create = conversation._create_optional_args

            def custom_create(*args, **kwargs):
                ptr = original_create(*args, **kwargs)

                if ptr is None:
                    ptr = (
                        lib.litert_lm_conversation_optional_args_create()
                    )

                    if not ptr:
                        raise RuntimeError(
                            "Failed to create LiteRT-LM optional arguments."
                        )

                lib.litert_lm_conversation_optional_args_set_visual_token_budget(
                    ptr,
                    self.visual_token_budget,
                )

                return ptr

            conversation._create_optional_args = custom_create

            message = litert_lm.Message.user(
                litert_lm.Contents(
                    [
                        litert_lm.Content.ImageFile(
                            str(image_path)
                        ),
                        litert_lm.Content.Text(
                            prompt
                        ),
                    ]
                )
            )

            start = time.perf_counter()

            response = conversation.send_message(
                message,
                max_output_tokens=max_output_tokens,
                thinking_config=litert_lm.ThinkingConfig(
                    enable_thinking=False,
                    thinking_token_budget=0,
                ),
            )

            elapsed = time.perf_counter() - start

            return {
                "response": response,
                "elapsed_time": elapsed,
                "visual_token_budget": self.visual_token_budget,
            }

        finally:
            conversation.close()

    def close(self) -> None:
        """Release LiteRT-LM resources."""

        if self.conversation is not None:
            self.conversation.close()
            self.conversation = None

        if self.engine is not None:
            self.engine.close()
            self.engine = None