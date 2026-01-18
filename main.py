from fasthtml.common import *
from monsterui.all import *

from backend.middleware import require_auth
from landingpage import landingPage
from frontend.signin import signinPage
from frontend.assets import assetsPage
from frontend.dashboard import dashboardPage
from frontend.profile import profilePage
import logging


# ==================================================
# LOGGING SETUP
# ==================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")


# ==================================================
# APP SETUP
# ==================================================
logger.info("Initializing FastHTML app")

app, rt = fast_app(hdrs=Theme.slate.headers(mode="dark"))

# IMPORTANT: import auth AFTER rt exists
import backend.auth
logger.info("Auth routes loaded")


# ==================================================
# FRONTEND ROUTES
# ==================================================
@rt("/")
def landing_page():
    logger.info("GET /")
    return landingPage()


@rt("/signin")
def signin_page():
    logger.info("GET /signin")
    return signinPage()


@rt("/assets")
def assets_page():
    logger.info("GET /assets")
    return assetsPage()


# ==================================================
# PROFILE (PROTECTED)
# ==================================================
@rt("/profile")
@require_auth
def profile(req):
    user = req.state.user
    logger.info("GET /profile | user=%s", user.email)

    payload = {
        "fullName": user.user_metadata.get("full_name", ""),
        "email": user.email,
        "profilePicture": user.user_metadata.get("avatar_url", ""),
        "plan": "Pro",
        "analysis_limit": "50 analyses / month",
        "subscription_status": "Active",
    }

    return profilePage(payload)


# ==================================================
# DASHBOARD (PROTECTED)
# ==================================================
@rt("/dashboard")
@require_auth
def dashboard(req):
    user = req.state.user
    logger.info("GET /dashboard | user=%s", user.email)
    return dashboardPage(user)


# ==================================================
# LOCAL DEV ONLY
# ==================================================
if __name__ == "__main__":
    logger.info("Starting local server")
    serve()
