"""
Business Analysis App
Built with FastHTML + MonsterUI
"""

from fasthtml.common import *
from monsterui.all import *
from design.navbar import reusable_navbar


# ==================================================
# APP SETUP
# ==================================================



# ==================================================
# ADD BUSINESS MODAL
# ==================================================
def add_business_modal():
    return Modal(
        ModalTitle("Add Business"),
        Div(
            Label("Business Name"),
            Input(placeholder="e.g. PriceWink"),

            Label("Description", cls="mt-3"),
            Textarea(
                placeholder="What does this business do?",
                rows=3
            ),

            Label("Industry / Type", cls="mt-3"),
            Input(placeholder="e.g. SaaS, E-commerce"),

            Label("Primary Goal", cls="mt-3"),
            Select(
                Option("Pricing intelligence"),
                Option("Competitor tracking"),
                Option("Positioning"),
                Option("Market research")
            ),

            cls="space-y-2"
        ),
        footer=DivFullySpaced(
            ModalCloseButton("Cancel", cls=ButtonT.ghost),
            Button("Save Business", cls=ButtonT.primary)
        ),
        id="add-business-modal"
    )


# ==================================================
# EDIT BUSINESS MODAL
# ==================================================
def edit_business_modal():
    return Modal(
        ModalTitle("Edit Business"),
        Div(
            Label("Business Name"),
            Input(),

            Label("Description", cls="mt-3"),
            Textarea(
                rows=3,
                placeholder="Update business description"
            ),

            Label("Industry / Type", cls="mt-3"),
            Input(placeholder="e.g. SaaS, E-commerce"),

            Hr(cls="my-4"),

            H4("Competitors", cls="font-semibold"),

            Textarea(
                rows=5,
                placeholder=(
                    "Paste competitor info here.\n"
                    "- Name\n"
                    "- Pricing\n"
                    "- Strategy\n"
                    "- Notes"
                )
            ),

            P(
                "You can paste raw notes, pricing tables, or strategy updates.",
                cls="text-xs text-slate-400"
            ),

            cls="space-y-2"
        ),
        footer=DivFullySpaced(
            ModalCloseButton("Close", cls=ButtonT.ghost),
            Button("Save Changes", cls=ButtonT.primary)
        ),
        id="edit-business-modal"
    )


# ==================================================
# ANALYSIS STAT CARDS
# ==================================================
def analysis_stats():
    def stat_card(title, value, subtitle, icon):
        return Card(
            DivLAligned(
                UkIcon(icon, height=24),
                Div(
                    H3(value, cls="text-2xl font-bold"),
                    P(title, cls="text-sm text-slate-600"),
                    P(subtitle, cls="text-xs text-slate-400")
                )
            )
        )

    stats = [
        stat_card("Total Analyses", "128", "Across all businesses", "activity"),
        stat_card("Active Businesses", "6", "Currently monitored", "briefcase"),
        stat_card("Competitors Tracked", "42", "Unique competitors", "users"),
        stat_card("Price Changes", "17", "Detected this week", "trending-up"),
        stat_card("Feature Changes", "9", "New or removed", "layers"),
        stat_card("Alerts Triggered", "4", "Needs attention", "bell"),
    ]

    return Grid(
        *stats,
        cols_sm=1,
        cols_md=2,
        cols_lg=3,
        gap=6
    )


# ==================================================
# BUSINESS CARD COMPONENT
# ==================================================
def business_card(
    name="Acme SaaS",
    description="Subscription-based analytics platform for small teams.",
    owner="John Doe",
    last_scan="Last scan: 2 days ago",
    tags=("SaaS", "Pricing", "Competitors")
):
    def Tags(items):
        return DivLAligned(map(Label, items))

    return Card(
        DivLAligned(
            A(
                Img(
                    src="https://picsum.photos/200/200?random=8",
                    style="width:200px"
                ),
                href="#"
            ),
            Div(cls="space-y-3 uk-width-expand")(
                H4(name),
                P(description, cls="text-slate-600"),
                DivFullySpaced(
                    map(Small, [owner, last_scan]),
                    cls=TextT.muted
                ),
                DivFullySpaced(
                    Tags(tags),
                    Button(
                        "Edit",
                        cls=(ButtonT.primary, "h-6"),
                        data_uk_toggle="target: #edit-business-modal"
                    )
                )
            )
        ),
        cls=CardT.hover
    )


# ==================================================
# ROUTE
# ==================================================

def assetsPage():
    return Div(

        reusable_navbar(),

        # Header
        Div(
            H2("Your Businesses", cls="text-3xl font-bold"),
            P(
                "Track pricing, positioning, and competitor movements "
                "for each business you manage.",
                cls="text-slate-500 max-w-2xl"
            ),
            Div(
                Button(
                    "Add Business",
                    cls=ButtonT.primary,
                    data_uk_toggle="target: #add-business-modal"
                ),
                cls="mt-6"
            ),
            cls="mb-12 space-y-3"
        ),

        # ===============================
        # ANALYSIS OVERVIEW
        # ===============================
        Div(
            H3("Analysis Overview", cls="text-xl font-semibold mb-4"),
            analysis_stats(),
            cls="mb-14"
        ),

        # ===============================
        # BUSINESS CARDS
        # ===============================
        Div(
            business_card(
                name="PriceWink",
                description="Competitor price monitoring for small businesses.",
                owner="You",
                last_scan="Last scan: Today",
                tags=("SaaS", "Pricing", "Monitoring")
            ),
            business_card(
                name="Devdan Tools",
                description="Internal tools helping non-technical users automate work.",
                owner="You",
                last_scan="Last scan: 5 days ago",
                tags=("Automation", "Productivity")
            ),
            business_card(
                name="MarketScout",
                description="Market intelligence for e-commerce brands.",
                owner="You",
                last_scan="Last scan: 1 week ago",
                tags=("E-commerce", "Trends", "Competitors")
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-6"
        ),

        # Modals (mounted once)
        add_business_modal(),
        edit_business_modal(),

        cls="w-full px-6 py-10"
    )


