"""
Business Analysis App - Assets Page
Built with FastHTML + MonsterUI
Now with real Supabase integration
"""

from fasthtml.common import *
from monsterui.all import *
from design.navbar import reusable_navbar


# ==================================================
# ADD BUSINESS MODAL
# ==================================================
def add_business_modal():
    return Modal(
        ModalTitle("Add Business"),
        Form(
            hx_post="/api/assets",
            hx_target="#business-cards",
            hx_swap="afterbegin"
        )(
            Div(
                Label("Business Name"),
                Input(name="name", placeholder="e.g. PriceWink", required=True),

                Label("Description", cls="mt-3"),
                Textarea(
                    name="description",
                    placeholder="What does this business do?",
                    rows=3
                ),

                Label("Industry / Type", cls="mt-3"),
                Input(name="type", placeholder="e.g. SaaS, E-commerce"),

                Hidden(name="value", value="0"),  # Default value

                cls="space-y-2"
            ),
            footer=DivFullySpaced(
                ModalCloseButton("Cancel", cls=ButtonT.ghost),
                Button("Save Business", type="submit", cls=ButtonT.primary)
            )
        ),
        id="add-business-modal"
    )


# ==================================================
# EDIT BUSINESS MODAL
# ==================================================
def edit_business_modal(asset_id="", name="", description="", type_=""):
    return Modal(
        ModalTitle("Edit Business"),
        Form(
            hx_put=f"/api/assets/{asset_id}",
            hx_target=f"#asset-{asset_id}",
            hx_swap="outerHTML"
        )(
            Div(
                Label("Business Name"),
                Input(name="name", value=name, required=True),

                Label("Description", cls="mt-3"),
                Textarea(
                    name="description",
                    rows=3,
                    placeholder="Update business description"
                )(description),

                Label("Industry / Type", cls="mt-3"),
                Input(name="type", value=type_, placeholder="e.g. SaaS, E-commerce"),

                cls="space-y-2"
            ),
            footer=DivFullySpaced(
                ModalCloseButton("Close", cls=ButtonT.ghost),
                Button("Save Changes", type="submit", cls=ButtonT.primary)
            )
        ),
        id=f"edit-business-modal-{asset_id}"
    )


# ==================================================
# BUSINESS CARD COMPONENT
# ==================================================
def business_card(
    asset_id,
    name="Acme SaaS",
    description="Subscription-based analytics platform for small teams.",
    type_="SaaS",
    created_at="2 days ago"
):
    return Card(
        DivLAligned(
            A(
                Img(
                    src=f"https://ui-avatars.com/api/?name={name}&background=random",
                    style="width:80px;height:80px;border-radius:8px;"
                ),
                href="#"
            ),
            Div(cls="space-y-3 uk-width-expand")(
                H4(name),
                P(description or "No description", cls="text-slate-600"),
                DivFullySpaced(
                    Small(f"Created {created_at}", cls=TextT.muted),
                    DivHStacked(
                        Button(
                            "Edit",
                            cls=(ButtonT.secondary, "h-8 px-3 text-sm"),
                            hx_get=f"/api/assets/{asset_id}/edit",
                            hx_target="#modal-container",
                            hx_swap="innerHTML"
                        ),
                        Button(
                            UkIcon("trash-2", height=16),
                            cls=(ButtonT.destructive, "h-8 px-3"),
                            hx_delete=f"/api/assets/{asset_id}",
                            hx_target=f"#asset-{asset_id}",
                            hx_swap="outerHTML",
                            hx_confirm="Are you sure you want to delete this business?"
                        ),
                        gap=2
                    )
                ),
                Label(type_ or "General", cls=LabelT.primary)
            )
        ),
        cls=CardT.hover,
        id=f"asset-{asset_id}"
    )


# ==================================================
# ANALYSIS STATS (will be dynamic later)
# ==================================================
def analysis_stats(stats=None):
    stats = stats or {
        "total_analyses": 0,
        "active_businesses": 0,
        "competitors_tracked": 0,
        "price_changes": 0,
        "feature_changes": 0,
        "alerts_triggered": 0
    }
    
    def stat_card(title, value, subtitle, icon):
        return Card(
            DivLAligned(
                UkIcon(icon, height=24),
                Div(
                    H3(str(value), cls="text-2xl font-bold"),
                    P(title, cls="text-sm text-slate-600"),
                    P(subtitle, cls="text-xs text-slate-400")
                )
            )
        )

    cards = [
        stat_card("Total Analyses", stats.get("total_analyses", 0), "Across all businesses", "activity"),
        stat_card("Active Businesses", stats.get("active_businesses", 0), "Currently monitored", "briefcase"),
        stat_card("Competitors Tracked", stats.get("competitors_tracked", 0), "Unique competitors", "users"),
        stat_card("Price Changes", stats.get("price_changes", 0), "Detected this week", "trending-up"),
        stat_card("Feature Changes", stats.get("feature_changes", 0), "New or removed", "layers"),
        stat_card("Alerts Triggered", stats.get("alerts_triggered", 0), "Needs attention", "bell"),
    ]

    return Grid(
        *cards,
        cols_sm=1,
        cols_md=2,
        cols_lg=3,
        gap=6
    )


# ==================================================
# MAIN PAGE
# ==================================================
def assetsPage(user_assets=None):
    user_assets = user_assets or []
    
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

        # Analysis Overview
        Div(
            H3("Analysis Overview", cls="text-xl font-semibold mb-4"),
            analysis_stats({
                "active_businesses": len(user_assets)
            }),
            cls="mb-14"
        ),

        # Business Cards
        Div(
            *[business_card(
                asset_id=asset.get("id"),
                name=asset.get("name", "Unnamed Business"),
                description=asset.get("description", ""),
                type_=asset.get("type", ""),
                created_at="Recently"  # You can format created_at timestamp
            ) for asset in user_assets],
            id="business-cards",
            cls="grid grid-cols-1 md:grid-cols-2 gap-6"
        ) if user_assets else Div(
            P("No businesses yet. Click 'Add Business' to get started!", 
              cls="text-slate-400 text-center py-12"),
            id="business-cards",
            cls="grid grid-cols-1 md:grid-cols-2 gap-6"
        ),

        # Modals
        add_business_modal(),
        Div(id="modal-container"),  # For dynamic edit modals

        cls="w-full px-6 py-10"
    )