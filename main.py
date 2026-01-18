# ==================================================
# APSW / APSWUTILS / FASTLITE STUBS — REQUIRED FOR VERCEL
# MUST BE FIRST - BEFORE ANY OTHER IMPORTS
# ==================================================
##
import sys
import types

# ---------------- apsw (native) ----------------
fake_apsw = types.ModuleType("apsw")
fake_apsw.ext = types.ModuleType("ext")
fake_apsw.bestpractice = types.ModuleType("bestpractice")
fake_apsw.unicode = types.ModuleType("unicode")
fake_apsw._unicode = types.ModuleType("_unicode")  # Add this for unicode module

sys.modules["apsw"] = fake_apsw
sys.modules["apsw.ext"] = fake_apsw.ext
sys.modules["apsw.bestpractice"] = fake_apsw.bestpractice
sys.modules["apsw.unicode"] = fake_apsw.unicode
sys.modules["apsw._unicode"] = fake_apsw._unicode

# ---------------- apswutils (package) ----------------
fake_apswutils = types.ModuleType("apswutils")
fake_apswutils.__path__ = []
fake_apswutils.Database = object
sys.modules["apswutils"] = fake_apswutils

# ---------------- apswutils.db ----------------
fake_apswutils_db = types.ModuleType("apswutils.db")

class NotFoundError(Exception):
    pass

fake_apswutils_db.Database = object
fake_apswutils_db.NotFoundError = NotFoundError

sys.modules["apswutils.db"] = fake_apswutils_db

# ---------------- apswutils.utils ----------------
fake_apswutils_utils = types.ModuleType("apswutils.utils")

def _noop(*args, **kwargs):
    return None

fake_apswutils_utils.rows_from_file = _noop
fake_apswutils_utils.TypeTracker = object
fake_apswutils_utils.Format = object

sys.modules["apswutils.utils"] = fake_apswutils_utils

# ---------------- fastlite ----------------
fake_fastlite = types.ModuleType("fastlite")
fake_fastlite.__path__ = []

# Stub out the main classes and functions
fake_fastlite.Database = object
fake_fastlite.database = _noop
fake_fastlite.NotFoundError = NotFoundError

# Core module
fake_fastlite_core = types.ModuleType("fastlite.core")
fake_fastlite_core.Database = object
fake_fastlite_core.database = _noop
fake_fastlite_core.NotFoundError = NotFoundError

sys.modules["fastlite"] = fake_fastlite
sys.modules["fastlite.core"] = fake_fastlite_core

# ==================================================
# NOW SAFE TO IMPORT FASTHTML / MONSTERUI
# ==================================================
from fasthtml.common import *
from monsterui.all import *
import logging

# Import your existing Supabase client
from dbase.supabase_client import supabase

from backend.middleware import require_auth
from landingpage import landingPage
from frontend.signin import signinPage
from frontend.assets import assetsPage
from frontend.dashboard import dashboardPage
from frontend.profile import profilePage

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


# ==================================================
# ASSETS PAGE (PROTECTED)
# ==================================================
@rt("/assets")
@require_auth
def assets_page(req):
    user = req.state.user
    logger.info("GET /assets | user=%s", user.email)
    
    try:
        # Fetch user's assets from Supabase
        assets_response = supabase.table("assets").select("*").eq("user_id", user.id).order("created_at", desc=True).execute()
        user_assets = assets_response.data if assets_response.data else []
        logger.info("Fetched %d assets for user", len(user_assets))
    except Exception as e:
        logger.error("Error fetching assets: %s", e)
        user_assets = []
    
    return assetsPage(user_assets)


# ==================================================
# PROFILE (PROTECTED)
# ==================================================
@rt("/profile")
@require_auth
def profile(req):
    user = req.state.user
    logger.info("GET /profile | user=%s", user.email)
    
    try:
        # Fetch user profile from Supabase
        response = supabase.table("profiles").select("*").eq("user_id", user.id).execute()
        
        if response.data and len(response.data) > 0:
            profile_data = response.data[0]
        else:
            # Create default profile if it doesn't exist
            profile_data = {
                "user_id": user.id,
                "plan": "Free",
                "analysis_limit": "10 analyses / month",
                "subscription_status": "Active"
            }
            supabase.table("profiles").insert(profile_data).execute()
            logger.info("Created new profile for user %s", user.email)
    
    except Exception as e:
        logger.error("Error fetching profile: %s", e)
        profile_data = {}
    
    payload = {
        "fullName": user.user_metadata.get("full_name", ""),
        "email": user.email,
        "profilePicture": user.user_metadata.get("avatar_url", ""),
        "plan": profile_data.get("plan", "Free"),
        "analysis_limit": profile_data.get("analysis_limit", "10 analyses / month"),
        "subscription_status": profile_data.get("subscription_status", "Active"),
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
    
    # Dashboard doesn't need assets, just pass user
    return dashboardPage(user)


# ==================================================
# API: GET ALL ASSETS
# ==================================================
@rt("/api/assets")
@require_auth
def get_assets(req):
    """Fetch all assets for the authenticated user"""
    user = req.state.user
    
    try:
        response = supabase.table("assets").select("*").eq("user_id", user.id).order("created_at", desc=True).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        logger.error("Error fetching assets: %s", e)
        return {"success": False, "error": str(e)}


# ==================================================
# API: CREATE ASSET (HTMX)
# ==================================================
@rt("/api/assets", methods=["POST"])
@require_auth
def create_asset(req, name: str, description: str = "", type: str = "", value: float = 0.0):
    """Create a new asset and return the card HTML"""
    user = req.state.user
    
    try:
        asset_data = {
            "user_id": user.id,
            "name": name,
            "description": description,
            "type": type,
            "value": value
        }
        
        response = supabase.table("assets").insert(asset_data).execute()
        logger.info("Created asset for user %s: %s", user.email, name)
        
        # Return the new business card HTML
        if response.data and len(response.data) > 0:
            new_asset = response.data[0]
            from frontend.assets import business_card
            return business_card(
                asset_id=new_asset.get("id"),
                name=new_asset.get("name", "Unnamed Business"),
                description=new_asset.get("description", ""),
                type_=new_asset.get("type", ""),
                created_at="Just now"
            )
        
        return Div("Error creating asset", cls="text-red-500")
        
    except Exception as e:
        logger.error("Error creating asset: %s", e)
        return Div(f"Error: {str(e)}", cls="text-red-500")


# ==================================================
# API: GET EDIT MODAL FOR ASSET
# ==================================================
@rt("/api/assets/{asset_id}/edit")
@require_auth
def get_edit_modal(req, asset_id: str):
    """Return edit modal HTML for a specific asset"""
    user = req.state.user
    
    try:
        # Verify ownership
        response = supabase.table("assets").select("*").eq("id", asset_id).eq("user_id", user.id).execute()
        
        if not response.data or len(response.data) == 0:
            return Div("Asset not found", cls="text-red-500")
        
        asset = response.data[0]
        from frontend.assets import edit_business_modal
        
        return edit_business_modal(
            asset_id=asset.get("id"),
            name=asset.get("name", ""),
            description=asset.get("description", ""),
            type_=asset.get("type", "")
        )
        
    except Exception as e:
        logger.error("Error fetching asset for edit: %s", e)
        return Div(f"Error: {str(e)}", cls="text-red-500")


# ==================================================
# API: UPDATE ASSET (HTMX)
# ==================================================
@rt("/api/assets/{asset_id}", methods=["PUT"])
@require_auth
def update_asset(req, asset_id: str, name: str = None, description: str = None, type: str = None, value: float = None):
    """Update an existing asset and return updated card"""
    user = req.state.user
    
    try:
        # First verify the asset belongs to the user
        check = supabase.table("assets").select("user_id").eq("id", asset_id).execute()
        
        if not check.data or check.data[0]["user_id"] != user.id:
            return Div("Unauthorized", cls="text-red-500")
        
        # Build update data
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if type is not None:
            update_data["type"] = type
        if value is not None:
            update_data["value"] = value
        
        if not update_data:
            return Div("No fields to update", cls="text-red-500")
        
        response = supabase.table("assets").update(update_data).eq("id", asset_id).execute()
        logger.info("Updated asset %s for user %s", asset_id, user.email)
        
        # Return updated card
        if response.data and len(response.data) > 0:
            updated_asset = response.data[0]
            from frontend.assets import business_card
            return business_card(
                asset_id=updated_asset.get("id"),
                name=updated_asset.get("name", "Unnamed Business"),
                description=updated_asset.get("description", ""),
                type_=updated_asset.get("type", ""),
                created_at="Updated"
            )
        
        return Div("Error updating asset", cls="text-red-500")
        
    except Exception as e:
        logger.error("Error updating asset: %s", e)
        return Div(f"Error: {str(e)}", cls="text-red-500")


# ==================================================
# API: DELETE ASSET (HTMX)
# ==================================================
@rt("/api/assets/{asset_id}", methods=["DELETE"])
@require_auth
def delete_asset(req, asset_id: str):
    """Delete an asset - returns empty for HTMX swap"""
    user = req.state.user
    
    try:
        # First verify the asset belongs to the user
        check = supabase.table("assets").select("user_id").eq("id", asset_id).execute()
        
        if not check.data or check.data[0]["user_id"] != user.id:
            return Div("Unauthorized", cls="text-red-500")
        
        supabase.table("assets").delete().eq("id", asset_id).execute()
        logger.info("Deleted asset %s for user %s", asset_id, user.email)
        
        # Return empty div (HTMX will swap and remove the element)
        return Div()
        
    except Exception as e:
        logger.error("Error deleting asset: %s", e)
        return Div(f"Error: {str(e)}", cls="text-red-500")


# ==================================================
# API: UPDATE PROFILE
# ==================================================
@rt("/api/profile", methods=["PUT"])
@require_auth
def update_profile(req, plan: str = None, analysis_limit: str = None):
    """Update user profile"""
    user = req.state.user
    
    try:
        update_data = {}
        if plan is not None:
            update_data["plan"] = plan
        if analysis_limit is not None:
            update_data["analysis_limit"] = analysis_limit
        
        if not update_data:
            return {"success": False, "error": "No fields to update"}
        
        # Check if profile exists
        check = supabase.table("profiles").select("id").eq("user_id", user.id).execute()
        
        if check.data:
            # Update existing profile
            response = supabase.table("profiles").update(update_data).eq("user_id", user.id).execute()
        else:
            # Create new profile
            update_data["user_id"] = user.id
            response = supabase.table("profiles").insert(update_data).execute()
        
        logger.info("Updated profile for user %s", user.email)
        return {"success": True, "data": response.data}
    except Exception as e:
        logger.error("Error updating profile: %s", e)
        return {"success": False, "error": str(e)}


# ==================================================
# HEALTH CHECK
# ==================================================
@rt("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test Supabase connection
        supabase.table("profiles").select("count", count="exact").limit(1).execute()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error("Health check failed: %s", e)
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# ==================================================
# LOCAL DEV ONLY
# ==================================================
if __name__ == "__main__":
    serve()