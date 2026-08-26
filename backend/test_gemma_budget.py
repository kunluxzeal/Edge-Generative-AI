import ctypes
import time

import litert_lm


MODEL_PATH = "/home/intelliscan/Documents/intelliscan/models/gemma-4-E2B-it.litertlm"
IMAGE_PATH = "/home/intelliscan/Documents/intelliscan/test_images/rotten_orange.jpg"


def run_test(budget: int) -> None:
    print("\n" + "=" * 60)
    print(f"VISUAL TOKEN BUDGET: {budget}")
    print("=" * 60)

    cpu = litert_lm.interfaces.CPU(thread_count=4)

    engine = litert_lm.Engine(
        MODEL_PATH,
        backend=cpu,
        vision_backend=cpu,
        max_num_images=1,
    )

    conversation = engine.create_conversation()

    lib = conversation._lib

    lib.litert_lm_conversation_optional_args_create.restype = ctypes.c_void_p
    lib.litert_lm_conversation_optional_args_create.argtypes = []

    lib.litert_lm_conversation_optional_args_set_visual_token_budget.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
    ]

    lib.litert_lm_conversation_optional_args_delete.argtypes = [
        ctypes.c_void_p
    ]

    args_ptr = lib.litert_lm_conversation_optional_args_create()

    if not args_ptr:
        raise RuntimeError("Failed to create optional args")

    lib.litert_lm_conversation_optional_args_set_visual_token_budget(
        args_ptr,
        budget,
    )

    original_create = conversation._create_optional_args
    original_delete = conversation._delete_optional_args

    def custom_create(*args, **kwargs):
        return args_ptr

    def custom_delete(ptr):
        # Do nothing here.
        # We will delete args_ptr ourselves.
        pass

    conversation._create_optional_args = custom_create
    conversation._delete_optional_args = custom_delete

    try:
        message = litert_lm.Message.user(
            litert_lm.Contents([
                litert_lm.Content.ImageFile(IMAGE_PATH),
                litert_lm.Content.Text(
                    "Return only GOOD or DEFECTIVE."
                ),
            ])
        )

        start = time.perf_counter()

        response = conversation.send_message(
            message,
            thinking_config=litert_lm.ThinkingConfig(
                enable_thinking=False
            ),
        )

        elapsed = time.perf_counter() - start

        print("\nRESPONSE:")
        print(response)

        print(f"Inference time: {elapsed:.3f} seconds")

    finally:
        conversation._create_optional_args = original_create
        conversation._delete_optional_args = original_delete

        lib.litert_lm_conversation_optional_args_delete(args_ptr)

        conversation.close()
        engine.close()


for budget in [70, 140, 280]:
    run_test(budget)