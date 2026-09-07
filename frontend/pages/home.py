# import reflex as rx


# def home() -> rx.Component:
#     return rx.box(
#         # Top bar
#         rx.hstack(
#             rx.spacer(),

#             rx.button(
#                 rx.vstack(
#                     rx.image(
#                         src="/settings_icon.png",
#                         width="40px",
#                         height="40px",
#                     ),
#                     rx.text(
#                         "Settings",
#                         size="2",
#                     ),
#                     spacing="0",
#                     align="center",
#                 ),
#                 size="4",
#                 on_click=rx.redirect("/settings"),
#                 variant="ghost",
#             ),

#             width="100%",
#             padding="20px",
#         ),

#         # Main content
#         rx.box(
#             rx.vstack(
#                 # iScan
#                 rx.heading(
#                     "intelliScan",
#                     size="9",
#                     style={
#                         "font_size": "100px",
#                     },
#                     weight="bold",
#                     color="accent",
#                     margin_top="120px"
#                 ),

#                 # Subtitle
#                 rx.text(
#                     "Offline Edge AI",
#                     size="5",
#                     color="gray",
#                     margin_top="50px",
#                 ),

#                 # Description
#                 rx.text(
#                     "Intelligent crop inspection with on-device AI.",
#                     size="3",
#                     color="gray",
#                     text_align="center",
#                     max_width="500px",
#                     margin_top="35px",
#                 ),

#                 # Start button
#                 rx.button(
#                     "Start Inspection",
#                     size="4",
#                     on_click=rx.redirect("/inspection"),
#                     width="220px",
#                     height="52px",
#                     margin_top="50px",
#                 ),

                

#                 align="center",
#             ),

#             width="100%",
#             flex="1",
#             padding_top="40px",
#         ),

#         width="100%",
#         min_height="100vh",


#          background=(
#             "radial-gradient("
#             "circle at 50% 35%, "
#             "rgba(37, 99, 235, 0.12), "
#             "transparent 40%"
#             "), "
#             "linear-gradient("
#             "135deg, "
#             "#070B14 0%, "
#             "#0F172A 50%, "
#             "#0B1120 100%"
#             ")"
#         ),
#         # display="flex",
#         # flex_direction="column",
#     )


import reflex as rx


def home() -> rx.Component:
    return rx.box(
        # --------------------------------------------------
        # Top navigation
        # --------------------------------------------------
        rx.hstack(
            rx.text(
                "intelliScan",
                font_size="22px",
                font_weight="700",
                color="#F8FAFC",
                letter_spacing="-0.02em",
            ),

            rx.spacer(),

            rx.button(
                rx.hstack(
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
                    
                 
                    spacing="0",
                    align="center",
                ),
                variant="ghost",
                color="#CBD5E1",
                on_click=rx.redirect("/settings"),
                _hover={
                    "background": "rgba(255,255,255,0.06)",
                },
            ),

            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_x="32px",
            padding_y="24px",
            align="center",
        ),

        # --------------------------------------------------
        # Hero section
        # --------------------------------------------------
        rx.box(
            rx.vstack(
                # Badge
                rx.box(
                    rx.hstack(
                        rx.box(
                            width="7px",
                            height="7px",
                            border_radius="50%",
                            background="#3B82F6",
                        ),
                        rx.text(
                            "OFFLINE EDGE AI",
                            font_size="12px",
                            font_weight="600",
                            color="#93C5FD",
                            letter_spacing="0.08em",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    padding_x="14px",
                    padding_y="7px",
                    border="1px solid rgba(59,130,246,0.25)",
                    border_radius="999px",
                    background="rgba(59,130,246,0.08)",
                ),

                # Main title
                rx.heading(
                    "intelliScan",
                    weight="bold",
                    color="#F8FAFC",
                    text_align="center",
                    style={
                        "font_size": "clamp(64px, 10vw, 112px)",
                        "line_height": "0.95",
                        "letter_spacing": "-0.06em",
                    },
                    margin_top="28px",
                ),

                # Subtitle
                rx.text(
                    "Intelligent Product Inspection System",
                    font_size="28px",
                    font_weight="600",
                    color="#60A5FA",
                    text_align="center",
                    line_height="1.2",
                    margin_top="20px",
                ),

                # Description
                rx.text(
                    "Inspect product quality "
                    "directly on the edge with multimodal AI.",
                    font_size="16px",
                    color="#94A3B8",
                    text_align="center",
                    line_height="1.7",
                    max_width="560px",
                    width="100%",
                    margin_top="18px",
                ),

                # CTA
                rx.button(
                    rx.hstack(
                        rx.text(
                            "Start Inspection",
                            font_size="16px",
                            font_weight="600",
                        ),
                        rx.text(
                            "→",
                            font_size="22px",
                            line_height="1",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    on_click=rx.redirect("/inspection"),
                    width="240px",
                    height="58px",
                    margin_top="38px",
                    background="#3B82F6",
                    color="#FFFFFF",
                    border_radius="14px",
                    border="none",
                    box_shadow="0 12px 30px rgba(59,130,246,0.22)",
                    _hover={
                        "background": "#2563EB",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 16px 35px rgba(59,130,246,0.30)",
                    },
                ),

                # Supporting text
                rx.text(
                    "Fast  •  Private  •  Runs locally",
                    font_size="13px",
                    color="#64748B",
                    text_align="center",
                    margin_top="18px",
                ),

                width="100%",
                max_width="720px",
                align="center",
                justify="center",
            ),

            # This is what makes the hero area centered.
            width="100%",
            display="flex",
            justify_content="center",
            align_items="center",
            flex="1",
            padding_x="24px",
            padding_y="60px",
        ),

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------
        rx.hstack(
            rx.text(
                "Powered by Gemma 4",
                font_size="12px",
                color="#475569",
            ),

            rx.spacer(),

            rx.text(
                "innov8hub",
                font_size="12px",
                color="#475569",
            ),

            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_x="32px",
            padding_y="18px",
            border_top="1px solid rgba(148,163,184,0.08)",
        ),

        # --------------------------------------------------
        # Background
        # --------------------------------------------------
        width="100%",
        min_height="100vh",
        display="flex",
        flex_direction="column",
        background=(
            "radial-gradient("
            "circle at 50% 35%, "
            "rgba(59,130,246,0.13), "
            "transparent 32%"
            "), "
            "radial-gradient("
            "circle at 85% 80%, "
            "rgba(14,116,144,0.08), "
            "transparent 25%"
            "), "
            "linear-gradient("
            "135deg, "
            "#020617 0%, "
            "#07111F 50%, "
            "#0B1729 100%"
            ")"
        ),
    )