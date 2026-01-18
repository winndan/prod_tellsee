from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

def signinPage():
    # ----------------------------------------------
    # LEFT PANEL (IMAGE + OVERLAY)
    # ----------------------------------------------
    left_panel = Div(
        cls="relative hidden lg:block h-full"
    )(
        Img(
            src="https://images.unsplash.com/photo-1723785735443-16ffd373f398?q=80&w=1167&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            cls="absolute inset-0 h-full w-full object-cover",
            alt="Auth background"
        ),
        Div(cls="absolute inset-0 bg-gradient-to-b from-black/80 to-black/60"),
        Div(
            H2(
                "Understand your business at a glance.",
                cls="text-white text-4xl font-semibold leading-tight"
            ),
            P(
                "Track competitors, pricing, and positioning — all in one place.",
                cls="text-white/70 max-w-md mt-4 text-lg"
            ),
            cls="absolute bottom-12 left-12 right-12"
        )
    )

    # ----------------------------------------------
    # RIGHT PANEL (DARK AUTH CARD)
    # ----------------------------------------------
    right_panel = Div(
        cls="flex items-center justify-center px-6 sm:px-10 relative"
    )(
        # 🔙 Back button (top-left)
        A(
            Div(
                UkIcon("arrow-left", cls="mr-2"),
                Span("Back"),
                cls="flex items-center gap-2 text-zinc-400 hover:text-white text-sm"
            ),
            href="/",
            cls="absolute top-6 left-6"
        ),

        Div(
            cls=(
                "w-full max-w-md space-y-8 rounded-xl "
                "border border-zinc-800 bg-zinc-950 p-8 "
                "shadow-2xl shadow-black/40"
            )
        )(
            # Header
            DivVStacked(
                Img(
                    src="https://www.svgrepo.com/show/475656/google-color.svg",
                    cls="h-12 w-12"
                ),
                H3(
                    "Sign in to your account",
                    cls="text-2xl font-semibold tracking-tight text-white"
                ),
                Small(
                    "Use your Google account to continue",
                    cls="text-zinc-400"
                ),
                cls="items-center space-y-3"
            ),

            Divider(cls="border-zinc-800"),

            # Google Button
            A(
                Button(
                    Div(
                        Img(
                            src="https://www.svgrepo.com/show/475656/google-color.svg",
                            cls="h-5 w-5"
                        ),
                        Span("Continue with Google"),
                        cls="flex items-center justify-center gap-3"
                    ),
                    cls=(
                        ButtonT.default,
                        "w-full py-3 text-base "
                        "bg-zinc-900 text-white border border-zinc-800 "
                        "hover:bg-zinc-800"
                    )
                ),
                href="/login"
            ),

            # Footer text
            Small(
                Span("By continuing, you agree to our "),
                A("Terms of Service", href="#", cls="text-zinc-400 hover:text-white"),
                Span(" and "),
                A("Privacy Policy", href="#", cls="text-zinc-400 hover:text-white"),
                Span("."),
                cls="text-zinc-500 text-center block leading-relaxed"
            )
        )
    )

    # ----------------------------------------------
    # PAGE WRAPPER
    # ----------------------------------------------
    return (
        Title("Sign In"),
        Grid(
            left_panel,
            right_panel,
            cols="1 lg:2",
            gap=0,
            cls="min-h-screen bg-black"
        )
    )
