import reflex as rx


def settings() -> rx.Component:
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
                        rx.icon("scan-search", size=18),
                        rx.text("Inspection"),
                        spacing="2",
                        align="center",
                    ),
                    variant="ghost",
                    color="#CBD5E1",
                    on_click=rx.redirect("/inspection"),
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
                        "SYSTEM CONFIGURATION",
                        font_size="11px",
                        font_weight="700",
                        color="#60A5FA",
                        letter_spacing="0.12em",
                    ),

                    rx.heading(
                        "Settings",
                        size="8",
                        weight="bold",
                        color="#F8FAFC",
                    ),

                    rx.text(
                        "Configure camera, AI inference, and system options.",
                        font_size="15px",
                        color="#94A3B8",
                        line_height="1.6",
                    ),

                    spacing="2",
                    align="start",
                ),

                width="100%",
            ),

            # ==================================================
            # CAMERA SETTINGS
            # ==================================================
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "camera",
                            size=20,
                            color="#60A5FA",
                        ),

                        rx.vstack(
                            rx.text(
                                "Camera",
                                font_size="17px",
                                font_weight="700",
                                color="#F8FAFC",
                            ),
                            rx.text(
                                "Configure the IMX477 camera.",
                                font_size="13px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        spacing="3",
                        align="center",
                    ),

                    rx.divider(),

                    # Preview resolution
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Preview Resolution",
                                font_size="14px",
                                font_weight="600",
                                color="#E2E8F0",
                            ),
                            rx.text(
                                "Resolution used for the live camera view.",
                                font_size="12px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        rx.spacer(),

                        rx.select(
                            ["320 × 240", "640 × 480", "1280 × 720"],
                            default_value="640 × 480",
                            width="180px",
                        ),

                        width="100%",
                        align="center",
                    ),

                    # Inspection resolution
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Inspection Resolution",
                                font_size="14px",
                                font_weight="600",
                                color="#E2E8F0",
                            ),
                            rx.text(
                                "Resolution sent to Gemma for analysis.",
                                font_size="12px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        rx.spacer(),

                        rx.select(
                            ["164 × 148", "320 × 240", "640 × 480"],
                            default_value="320 × 240",
                            width="180px",
                        ),

                        width="100%",
                        align="center",
                    ),

                    width="100%",
                    spacing="5",
                ),

                width="100%",
                padding="24px",
                border="1px solid rgba(148,163,184,0.10)",
                border_radius="18px",
                background="rgba(15,23,42,0.72)",
            ),

            # ==================================================
            # AI SETTINGS
            # ==================================================
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "brain",
                            size=20,
                            color="#60A5FA",
                        ),

                        rx.vstack(
                            rx.text(
                                "AI Inference",
                                font_size="17px",
                                font_weight="700",
                                color="#F8FAFC",
                            ),
                            rx.text(
                                "Configure Gemma 4 vision inference.",
                                font_size="13px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        spacing="3",
                        align="center",
                    ),

                    rx.divider(),

                    # Visual token budget
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Visual Token Budget",
                                font_size="14px",
                                font_weight="600",
                                color="#E2E8F0",
                            ),
                            rx.text(
                                "Controls the visual information processed by Gemma.",
                                font_size="12px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        rx.spacer(),

                        rx.select(
                            ["70", "140"],
                            default_value="70",
                            width="120px",
                        ),

                        width="100%",
                        align="center",
                    ),

                    # CPU threads
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "CPU Threads",
                                font_size="14px",
                                font_weight="600",
                                color="#E2E8F0",
                            ),
                            rx.text(
                                "CPU threads allocated to LiteRT-LM.",
                                font_size="12px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        rx.spacer(),

                        rx.select(
                            ["2", "4", "6", "8"],
                            default_value="4",
                            width="120px",
                        ),

                        width="100%",
                        align="center",
                    ),

                    width="100%",
                    spacing="5",
                ),

                width="100%",
                padding="24px",
                border="1px solid rgba(148,163,184,0.10)",
                border_radius="18px",
                background="rgba(15,23,42,0.72)",
            ),

            # ==================================================
            # SYSTEM STATUS
            # ==================================================
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "activity",
                            size=20,
                            color="#60A5FA",
                        ),

                        rx.vstack(
                            rx.text(
                                "System Status",
                                font_size="17px",
                                font_weight="700",
                                color="#F8FAFC",
                            ),
                            rx.text(
                                "Current iScan service status.",
                                font_size="13px",
                                color="#64748B",
                            ),
                            spacing="1",
                            align="start",
                        ),

                        spacing="3",
                        align="center",
                    ),

                    rx.divider(),

                    # Camera status
                    rx.hstack(
                        rx.text(
                            "Camera",
                            font_size="14px",
                            color="#CBD5E1",
                        ),

                        rx.spacer(),

                        rx.hstack(
                            rx.box(
                                width="8px",
                                height="8px",
                                border_radius="999px",
                                background="#22C55E",
                            ),
                            rx.text(
                                "Connected",
                                font_size="13px",
                                color="#22C55E",
                                font_weight="600",
                            ),
                            spacing="2",
                            align="center",
                        ),

                        width="100%",
                    ),

                    # Gemma status
                    rx.hstack(
                        rx.text(
                            "Gemma 4",
                            font_size="14px",
                            color="#CBD5E1",
                        ),

                        rx.spacer(),

                        rx.hstack(
                            rx.box(
                                width="8px",
                                height="8px",
                                border_radius="999px",
                                background="#22C55E",
                            ),
                            rx.text(
                                "Loaded",
                                font_size="13px",
                                color="#22C55E",
                                font_weight="600",
                            ),
                            spacing="2",
                            align="center",
                        ),

                        width="100%",
                    ),

                    # Backend
                    rx.hstack(
                        rx.text(
                            "Backend API",
                            font_size="14px",
                            color="#CBD5E1",
                        ),

                        rx.spacer(),

                        rx.hstack(
                            rx.box(
                                width="8px",
                                height="8px",
                                border_radius="999px",
                                background="#22C55E",
                            ),
                            rx.text(
                                "Connected",
                                font_size="13px",
                                color="#22C55E",
                                font_weight="600",
                            ),
                            spacing="2",
                            align="center",
                        ),

                        width="100%",
                    ),

                    width="100%",
                    spacing="4",
                ),

                width="100%",
                padding="24px",
                border="1px solid rgba(148,163,184,0.10)",
                border_radius="18px",
                background="rgba(15,23,42,0.72)",
            ),

            # Back button
            rx.button(
                rx.hstack(
                    rx.icon("arrow-left", size=18),
                    rx.text(
                        "Back to Inspection",
                        font_size="15px",
                    ),
                    spacing="2",
                    align="center",
                ),
                on_click=rx.redirect("/inspection"),
                variant="soft",
                color_scheme="blue",
                width="220px",
                height="48px",
                margin_top="4px",
            ),

            spacing="6",
            width="100%",
            max_width="1000px",
            padding_x="24px",
            padding_y="36px",
            margin="0 auto",
            align="stretch",
        ),

        # ==================================================
        # BACKGROUND
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