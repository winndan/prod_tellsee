from fasthtml.common import *
from monsterui.all import *


def reusable_navbar():
    return NavBar(

        # ---------------------------------
        # NAV LINKS
        # ---------------------------------
        A("Dashboard", href="/dashboard"),
        A("Assets", href="/assets"),
        A("Profile", href="/profile"),

        Button(
            "Logout",
            hx_post="/logout",
            hx_swap="none",
            hx_trigger="click",
            cls=(
                ButtonT.sm,
                "bg-[#3b82f6] hover:bg-[#2563eb] text-white border-none"
            )
        ),

        # ---------------------------------
        # BRAND
        # ---------------------------------
        brand=DivLAligned(
            Img(
                src="/assets/logo.png",
                alt="Tellsee",
                cls="h-8 w-8 rounded-md"
            ),
            Strong("Tellsee", cls="text-lg tracking-tight"),
            cls="gap-3"
        ),

        # ---------------------------------
        # OPTIONS
        # ---------------------------------
        sticky=True,
        uk_scrollspy_nav=True,
        scrollspy_cls=ScrollspyT.bold,
    )
