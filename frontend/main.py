import reflex as rx

from pages.home import home

from pages.settings import settings
from pages.inspection import inspection


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        gray_color="slate",
        radius="large",
        scaling="100%",
        has_background=True,
    )
)

app.add_page(
    home,
    route="/",
    title="intelliScan",
)


app.add_page(
    settings,
    route="/settings",
    title="Settings",
)

app.add_page(
    inspection,
    route="/inspection",
    title="Inspection",
)