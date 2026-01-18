"""
Profile Page
Built with FastHTML + MonsterUI
"""

from fasthtml.common import *
from monsterui.all import *
from design.navbar import reusable_navbar


def profilePage(user_data=None):
    user_data = user_data or {}

    # ----------------------------------------------
    # Helpers
    # ----------------------------------------------
    def get_profile_picture_url(user_data):
        pic = user_data.get("profilePicture")
        if pic and pic.strip():
            return pic
        initials = user_data.get("fullName") or "Guest"
        return f"https://avatars.dicebear.com/api/initials/{initials}.svg"

    def FormSectionDiv(*c, cls="space-y-2", **kwargs):
        return Div(*c, cls=cls, **kwargs)

    def StyledCard(title, subtitle, *content):
        return Card(
            Div(
                Div(cls="h-1 w-full bg-primary rounded-t-lg"),
                Div(
                    H3(title, cls="mt-4"),
                    Subtitle(subtitle, cls="text-primary"),
                    DividerLine(),
                    Form(*content, cls="space-y-3"),
                    cls="p-6"
                )
            ),
            cls="hover:shadow-lg transition-shadow duration-200"
        )

    # ----------------------------------------------
    # Sections
    # ----------------------------------------------
    profile_section = StyledCard(
        "Profile",
        "This is how others will see you.",
        FormSectionDiv(
            LabelInput(
                "Username",
                id="username",
                value=user_data.get("fullName", ""),
            ),
            P("This is your public display name.", cls="text-primary")
        ),
        FormSectionDiv(
            FormLabel("Email"),
            Input(value=user_data.get("email", ""), readonly=True),
            P("This is your registered email address.", cls="text-primary")
        ),
        FormSectionDiv(
            FormLabel("Profile Picture"),
            Img(
                src=get_profile_picture_url(user_data),
                cls="rounded-full object-cover ring-2 ring-primary/20",
                height=96,
                width=96,
            ),
            P("Fetched from your Google account.", cls="text-primary")
        )
    )

    subscription_section = StyledCard(
        "Subscription",
        "Your current plan and usage limits.",
        FormSectionDiv(
            FormLabel("Current Plan"),
            Input(value=user_data.get("plan", "Free"), readonly=True)
        ),
        FormSectionDiv(
            FormLabel("Monthly Analysis Limit"),
            Input(value=user_data.get("analysis_limit", "5 / month"), readonly=True)
        ),
        FormSectionDiv(
            FormLabel("Status"),
            Input(value=user_data.get("subscription_status", "Active"), readonly=True)
        ),
        FormSectionDiv(
            Button("Manage Subscription", cls=ButtonT.primary),
            P("Billing is handled securely.", cls="text-xs text-slate-400")
        )
    )

    return Container(
        reusable_navbar(),
        Div(
            profile_section,
            subscription_section,
            cls="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10"
        ),
        cls="max-w-6xl px-4"
    )
