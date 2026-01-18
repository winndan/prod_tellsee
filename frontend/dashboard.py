from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
from design.navbar import reusable_navbar


def dashboardPage(user):

    # ==================================================
    # ACTION BUTTONS
    # ==================================================
    bottom_buttons = Div(
        Button("Analyze", cls=ButtonT.primary),
        Button(UkIcon(icon="history"), cls=ButtonT.secondary),
        cls="flex justify-center items-center gap-x-3 mt-6"
    )

    # ==================================================
    # RIGHT SIDEBAR
    # ==================================================
    rsidebar = NavContainer(
        Div(
            H3("Competitor Settings", cls="text-lg font-semibold text-center lg:text-left"),
            P(
                "Choose which competitors and signals to analyze.",
                cls="text-slate-400 text-sm mt-1 text-center lg:text-left"
            ),
            cls="mb-4"
        ),

        Select(
            Optgroup(
                (
                    Option("SaaS Pricing Pages"),
                    Option("Landing Pages"),
                    Option("E-commerce Listings"),
                    Option("Marketplace Products"),
                ),
                label="Website Type"
            ),
            label="Competitor Source",
            searchable=True,
        ),

        Div(
            Strong("Tracked Competitors", cls="text-sm"),
            Ul(
                Li("Stripe"),
                Li("Paddle"),
                Li("Lemon Squeezy"),
                Li("Gumroad"),
                cls="space-y-2 text-slate-400 text-sm mt-3"
            ),
            cls="mt-4"
        ),

        Div(
            Strong("Analyze Signals", cls="text-sm"),
            Ul(
                Li("Plan price changes"),
                Li("Feature gating per tier"),
                Li("Free vs paid limits"),
                Li("Discounts & promos"),
                Li("Trial duration"),
                cls="space-y-2 text-slate-400 text-sm mt-3"
            ),
            cls="mt-4"
        ),

        bottom_buttons,
        cls="space-y-6"
    )

    # ==================================================
    # MAIN CONTENT
    # ==================================================
    main_content = Div(
        Div(
            H2("Competitor Analysis", cls="text-3xl font-bold text-center"),
            P(
                f"Logged in as {user.email}",
                cls="text-slate-500 mt-1 text-sm text-center"
            ),
            P(
                "Paste a competitor page or product details to analyze pricing, features, and positioning.",
                cls="text-slate-400 mt-2 max-w-2xl mx-auto text-center"
            ),
            cls="mb-6"
        ),
        Textarea(
            cls="uk-textarea resize-none p-4 h-[300px] sm:h-[400px] lg:h-[700px]",
            placeholder="Paste your competitor URL, pricing page, or product description here…",
        ),
        cls="flex-1 w-full"
    )

    return Div(
        reusable_navbar(),
        Div(
            main_content,
            Hr(cls="w-full border-slate-700 my-6 lg:hidden"),
            Div(rsidebar, cls="w-full lg:w-[320px] shrink-0 lg:mt-12"),
            cls="flex flex-col lg:flex-row items-start gap-6 w-full px-4 sm:px-6 py-6"
        ),
        cls="max-w-full"
    )
