# ==================================================
# APSW / APSWUTILS COMPLETE STUB — REQUIRED FOR VERCEL
# MUST BE FIRST
# ==================================================
import sys
import types

# ---------------- apsw (native) ----------------
fake_apsw = types.ModuleType("apsw")
fake_apsw.ext = types.ModuleType("ext")
fake_apsw.bestpractice = types.ModuleType("bestpractice")
fake_apsw.unicode = types.ModuleType("unicode")

sys.modules["apsw"] = fake_apsw
sys.modules["apsw.ext"] = fake_apsw.ext
sys.modules["apsw.bestpractice"] = fake_apsw.bestpractice
sys.modules["apsw.unicode"] = fake_apsw.unicode

# ---------------- apswutils (package) ----------------
fake_apswutils = types.ModuleType("apswutils")
fake_apswutils.__path__ = []          # mark as package
fake_apswutils.Database = object      # used by fasthtml
sys.modules["apswutils"] = fake_apswutils

# ---------------- apswutils.db ----------------
fake_apswutils_db = types.ModuleType("apswutils.db")
fake_apswutils_db.Database = object
sys.modules["apswutils.db"] = fake_apswutils_db

# ---------------- apswutils.utils ----------------
fake_apswutils_utils = types.ModuleType("apswutils.utils")

def _noop(*args, **kwargs):
    return None

fake_apswutils_utils.rows_from_file = _noop
fake_apswutils_utils.TypeTracker = object
fake_apswutils_utils.Format = object

sys.modules["apswutils.utils"] = fake_apswutils_utils

# ==================================================
# NOW SAFE TO IMPORT FASTHTML / MONSTERUI
# ==================================================
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

app, rt = fast_app(
    hdrs=Theme.slate.headers(mode="dark")
)

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
