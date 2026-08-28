import reflex as rx

def home() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "IntelliScan",
                size ="9",
                weight="bold",
            ),

            rx.text(
                "Offline Multimodal Edge AI",
                size="5",
                color="gray",
            ),

            rx.text(
                "Intelligent crop inspection with on-device AI.",
                size="3",
                color="gray",
                text_align="center"
            ),

            rx.button(
                "start Inspection",
                size="4",
                on_click=rx.redirect("/inspection"),
                width = "220px",
                height="52px",
            ),
            spacing="6",
            align="center",
        ),

        width = "100%",
        min_height="100vh",

    )

