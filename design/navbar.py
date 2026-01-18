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

        # ---------------------------------
        # LOGOUT BUTTON
        # ---------------------------------
        # Choose ONE of these options:
        
        # OPTION A: Regular Link (Simpler, More Reliable) ✅ RECOMMENDED
        A(
            Button(
                "Logout",
                cls=(
                    ButtonT.sm,
                    "bg-[#3b82f6] hover:bg-[#2563eb] text-white border-none"
                )
            ),
            href="/logout"
        ),
        
        # OPTION B: HTMX (If you prefer HTMX everywhere)
        # Uncomment this and remove OPTION A above
        # Button(
        #     "Logout",
        #     hx_get="/logout",      # Changed to GET (or use POST, both work now)
        #     hx_trigger="click",
        #     cls=(
        #         ButtonT.sm,
        #         "bg-[#3b82f6] hover:bg-[#2563eb] text-white border-none"
        #     )
        # ),

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