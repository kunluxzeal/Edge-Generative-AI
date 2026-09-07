# import reflex as rx


# def inspection() -> rx.Component:
#     return rx.box(
#         # -----------------------------
#         # Top navigation bar
#         # -----------------------------
#         rx.hstack(
#             rx.heading(
#                 "intelliScan",
#                 size="6",
#             ),

#             rx.spacer(),

#             rx.button(
#                 "Settings",
#                 on_click=rx.redirect("/settings"),
#                 variant="soft",
#             ),

#             width="100%",
#             padding="20px",
#             align="center",
#         ),

#         # -----------------------------
#         # Main inspection area
#         # -----------------------------
#         rx.vstack(
#             rx.heading(
#                 "Crop Inspection",
#                 size="8",
#             ),

#             rx.text(
#                 "Position the crop in front of the camera and press Analyze.",
#                 color="gray",
#                 text_align="center",
#             ),

#             # Camera panels
#             rx.grid(
#                 # Live camera
#                 rx.vstack(
#                     rx.text(
#                         "LIVE CAMERA",
#                         size="2",
#                         weight="bold",
#                     ),

#                     rx.box(
#                         rx.image(
#                             src="http://127.0.0.1:8000/api/camera/stream",
#                             width="100%",
#                             height="100%",
#                             object_fit="cover",
#                         ),
#                         width="100%",
#                         aspect_ratio="4 / 3",
#                         overflow="hidden",
#                         border_radius="12px",
#                     ),

#                     align="start",
#                     spacing="2",
#                     width="100%",
#                 ),

#                 # Inspection image
#                 rx.vstack(
#                     rx.text(
#                         "INSPECTION IMAGE",
#                         size="2",
#                         weight="bold",
#                     ),

#                     rx.box(
#                         rx.image(
#                             src="http://127.0.0.1:8000/api/camera/inspection",
#                             width="100%",
#                             height="100%",
#                             object_fit="cover",
#                         ),
#                         width="100%",
#                         aspect_ratio="4 / 3",
#                         overflow="hidden",
#                         border_radius="12px",
#                     ),

#                     align="start",
#                     spacing="2",
#                     width="100%",
#                 ),

#                 columns="2",
#                 spacing="5",
#                 width="100%",
#             ),

#             # Analyze button
#             rx.button(
#                 "Analyze",
#                 size="4",
#                 width="220px",
#                 height="52px",
#                 margin_top="10px",
#             ),

#             # Result section
#             rx.box(
#                 rx.vstack(
#                     rx.hstack(
#                         rx.heading(
#                             "Inspection Result",
#                             size="5",
#                         ),

#                         rx.spacer(),

#                         rx.badge(
#                             "READY",
#                             color_scheme="blue",
#                             variant="soft",
#                         ),

#                         width="100%",
#                     ),

#                     rx.divider(),

#                     rx.grid(
#                         rx.vstack(
#                             rx.text(
#                                 "Crop",
#                                 size="2",
#                                 color="gray",
#                             ),
#                             rx.text(
#                                 "—",
#                                 size="5",
#                                 weight="bold",
#                             ),
#                             align="start",
#                         ),

#                         rx.vstack(
#                             rx.text(
#                                 "Condition",
#                                 size="2",
#                                 color="gray",
#                             ),
#                             rx.text(
#                                 "—",
#                                 size="5",
#                                 weight="bold",
#                             ),
#                             align="start",
#                         ),

#                         rx.vstack(
#                             rx.text(
#                                 "Defect",
#                                 size="2",
#                                 color="gray",
#                             ),
#                             rx.text(
#                                 "No inspection yet",
#                                 size="4",
#                             ),
#                             align="start",
#                         ),

#                         columns="3",
#                         spacing="6",
#                         width="100%",
#                     ),

#                     rx.divider(),

#                     rx.hstack(
#                         rx.text(
#                             "Inference time:",
#                             color="gray",
#                         ),
#                         rx.text("—"),
#                         spacing="2",
#                     ),

#                     width="100%",
#                     spacing="5",
#                 ),

#                 width="100%",
#                 padding="24px",
#                 border="1px solid",
#                 border_color=rx.color("gray", 6),
#                 border_radius="16px",
#             ),

#             spacing="5",
#             width="100%",
#             max_width="1200px",
#             padding="20px",
#             align="center",
#         ),

#         width="100%",
#         min_height="100vh",
#     )


import reflex as rx
from state.inspection_state import InspectionState


BACKEND_URL = "http://127.0.0.1:8000"


def inspection() -> rx.Component:
    return rx.box(
        # ==================================================
        # TOP NAVIGATION
        # ==================================================
        rx.hstack(
            rx.hstack(
                rx.box(
                    width="10px",
                    height="10px",
                    border_radius="999px",
                    background="#3B82F6",
                    box_shadow="0 0 12px rgba(59,130,246,0.8)",
                ),
                rx.text(
                    "intelliScan",
                    font_size="20px",
                    font_weight="700",
                    color="#F8FAFC",
                ),
                spacing="3",
                align="center",
            ),

            rx.spacer(),

            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("house", size=18),
                        rx.text("Home"),
                        spacing="2",
                        align="center",
                    ),
                    variant="ghost",
                    color="#CBD5E1",
                    on_click=rx.redirect("/"),
                ),

                rx.button(
                    rx.hstack(
                        rx.icon("settings", size=18),
                        rx.text("Settings"),
                        spacing="2",
                        align="center",
                    ),
                    variant="ghost",
                    color="#CBD5E1",
                    on_click=rx.redirect("/settings"),
                ),

                spacing="2",
                align="center",
            ),

            width="100%",
            max_width="1400px",
            margin="0 auto",
            padding_x="32px",
            padding_y="18px",
            align="center",
            border_bottom="1px solid rgba(148,163,184,0.08)",
        ),

        # ==================================================
        # MAIN CONTENT
        # ==================================================
        rx.vstack(
            # Page heading
            rx.box(
                rx.vstack(
                    rx.text(
                        "CROP INSPECTION",
                        font_size="12px",
                        font_weight="700",
                        color="#60A5FA",
                        letter_spacing="0.12em",
                    ),

                    rx.heading(
                        "Inspect your crop",
                        size="8",
                        weight="bold",
                        color="#F8FAFC",
                    ),

                    rx.text(
                        "Position the crop inside the camera view, "
                        "then capture an image for AI analysis.",
                        font_size="15px",
                        color="#94A3B8",
                        max_width="620px",
                        line_height="1.6",
                    ),

                    spacing="1",
                    align="start",
                ),

                width="100%",
            ),

            # ==================================================
            # CAMERA AREA
            # ==================================================
            rx.grid(
                # ------------------------------------------
                # LIVE CAMERA
                # ------------------------------------------
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.hstack(
                                rx.box(
                                    width="8px",
                                    height="8px",
                                    border_radius="999px",
                                    background="#22C55E",
                                ),
                                rx.text(
                                    "LIVE CAMERA",
                                    font_size="12px",
                                    font_weight="700",
                                    color="#E2E8F0",
                                    letter_spacing="0.06em",
                                ),
                                spacing="2",
                                align="center",
                            ),

                            rx.spacer(),

                            rx.badge(
                                "LIVE",
                                color_scheme="green",
                                variant="soft",
                            ),

                            width="100%",
                            align="center",
                        ),

                        rx.box(
                            rx.image(
                                src=f"{BACKEND_URL}/api/camera/stream",
                                width="100%",
                                height="100%",
                                object_fit="cover",
                            ),
                            width="100%",
                            height="100%",
                            min_height="0",
                            #aspect_ratio="4 / 3",
                            overflow="hidden",
                            border_radius="14px",
                            background="#020617",
                        ),

                        rx.text(
                            "Live view from IMX477 camera",
                            font_size="12px",
                            color="#64748B",
                        ),

                        width="100%",
                        spacing="3",
                    ),

                    width="100%",
                    padding="18px",
                    border="1px solid rgba(148,163,184,0.10)",
                    border_radius="18px",
                    background="rgba(15,23,42,0.72)",
                    box_shadow="0 16px 40px rgba(0,0,0,0.20)",
                ),

                # ------------------------------------------
                # INSPECTION IMAGE
                # ------------------------------------------
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text(
                                "INSPECTION IMAGE",
                                font_size="12px",
                                font_weight="700",
                                color="#E2E8F0",
                                letter_spacing="0.06em",
                            ),

                            rx.spacer(),

                            rx.badge(
                                "CAPTURED",
                                color_scheme="blue",
                                variant="soft",
                            ),

                            width="100%",
                            align="center",
                        ),

                        rx.box(
                            rx.image(
                                src=InspectionState.inspection_image_url,
                                width="100%",
                                height="100%",
                                object_fit="cover",
                            ),
                            width="100%",
                            aspect_ratio="4 / 3",
                            overflow="hidden",
                            border_radius="14px",
                            background="#020617",
                        ),

                        rx.text(
                            "Frame submitted to Gemma 4",
                            font_size="12px",
                            color="#64748B",
                        ),

                        width="100%",
                        spacing="3",
                    ),

                    width="100%",
                    padding="18px",
                    border="1px solid rgba(148,163,184,0.10)",
                    border_radius="18px",
                    background="rgba(15,23,42,0.72)",
                    box_shadow="0 16px 40px rgba(0,0,0,0.20)",
                ),

                columns="2",
                spacing="5",
                width="100%",
            ),

            # ==================================================
            # ACTION AREA
            # ==================================================
            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.cond(
                             InspectionState.analyzing,
                            rx.spinner(size="2"),
                             rx.icon("scan-search", size=20),
                        ),
                        rx.text(
                            rx.cond(
                                InspectionState.analyzing,
                                "Analyzing",
                                "Analyze Crop",
                            ),
                            font_size="16px",
                            font_weight="700",
                        ),
                        spacing="3",
                        align="center",
                    ),

                    on_click = InspectionState.analyze,
                    disabled = InspectionState.analyzing,

                    width="240px",
                    height="56px",
                    border_radius="14px",
                    background="#3B82F6",
                    color="#FFFFFF",
                    box_shadow="0 12px 28px rgba(59,130,246,0.22)",
                    _hover={
                        "background": "#2563EB",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 16px 34px rgba(59,130,246,0.30)",
                    },
                ),

                rx.cond(
                    InspectionState.error_message != "",
                    rx.text(
                        InspectionState.error_message,
                        font_size="13px",
                        color="#F87171",
                        text_align="center",
                    ),
                ),

                rx.text(
                    "AI analysis runs entirely on the device.",
                    font_size="12px",
                    color="#64748B",
                ),

                spacing="2",
                align="center",
                padding_y="6px",
            ),

            # ==================================================
            # RESULT CARD
            # ==================================================
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "ANALYSIS RESULT",
                                font_size="11px",
                                font_weight="700",
                                color="#60A5FA",
                                letter_spacing="0.12em",
                            ),
                            rx.heading(
                                "Inspection Summary",
                                size="5",
                                color="#F8FAFC",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        rx.spacer(),

                        rx.badge(
                            InspectionState.status,
                            color_scheme="blue",
                            variant="soft",
                            radius="full",
                        ),

                        width="100%",
                        align="center",
                    ),

                    rx.divider(
                        margin_y="6px",
                    ),

                    # Result values
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Crop",
                                    font_size="12px",
                                    color="#64748B",
                                ),
                                rx.text(
                                    InspectionState.crop,
                                    font_size="20px",
                                    font_weight="700",
                                    color="#F8FAFC",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            padding="18px",
                            border_radius="14px",
                            background="rgba(2,6,23,0.45)",
                        ),

                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Condition",
                                    font_size="12px",
                                    color="#64748B",
                                ),
                                rx.badge(
                                    InspectionState.condition,
                                    color_scheme="blue",
                                    variant="soft",
                                    radius="full",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            padding="18px",
                            border_radius="14px",
                            background="rgba(2,6,23,0.45)",
                        ),

                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Defect",
                                    font_size="12px",
                                    color="#64748B",
                                ),
                                rx.text(
                                    InspectionState.defect,
                                    font_size="16px",
                                    font_weight="600",
                                    color="#E2E8F0",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            padding="18px",
                            border_radius="14px",
                            background="rgba(2,6,23,0.45)",
                        ),

                        columns="3",
                        spacing="4",
                        width="100%",
                    ),

                    # Metrics
                    rx.hstack(
                        rx.text(
                            "Inference time",
                            font_size="12px",
                            color="#64748B",
                        ),
                        rx.text(
                            InspectionState.inference_time,
                            font_size="13px",
                            font_weight="600",
                            color="#CBD5E1",
                        ),

                        rx.spacer(),

                        rx.text(
                            "Vision budget",
                            font_size="12px",
                            color="#64748B",
                        ),
                        rx.text(
                            InspectionState.visual_token_budget,
                            font_size="13px",
                            font_weight="600",
                            color="#CBD5E1",
                        ),

                        width="100%",
                        padding_top="4px",
                    ),

                    width="100%",
                    spacing="5",
                ),

                width="100%",
                padding="22px",
                border="1px solid rgba(148,163,184,0.10)",
                border_radius="18px",
                background="rgba(15,23,42,0.80)",
                box_shadow="0 18px 45px rgba(0,0,0,0.20)",
            ),

            spacing="2",
            width="100%",
            max_width="1280px",
            padding_x="24px",
            padding_y="15px",
            margin="0 auto",
            align="stretch",
        ),

        # ==================================================
        # PAGE BACKGROUND
        # ==================================================
        width="100%",
        min_height="100vh",
        background=(
            "radial-gradient("
            "circle at 50% 0%, "
            "rgba(37,99,235,0.10), "
            "transparent 32%"
            "), "
            "linear-gradient("
            "180deg, "
            "#020617 0%, "
            "#07111F 48%, "
            "#0B1729 100%"
            ")"
        ),
    )