from fasthtml.common import *
from main import rt
from dbase.supabase_client import supabase
import os
import logging

logger = logging.getLogger("auth")

# =============================
# DYNAMIC REDIRECT URL
# =============================
def get_base_url(req):
    """Get base URL from environment or request"""
    # 1. Check for explicit override (recommended for dev)
    override = os.getenv("BASE_URL")
    if override:
        logger.debug("Using BASE_URL override: %s", override)
        return override
    
    # 2. For production (Vercel)
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        logger.debug("Using Vercel URL: https://%s", vercel_url)
        return f"https://{vercel_url}"
    
    # 3. For local development - detect from request
    host = req.headers.get("host", "localhost:5001")
    
    # Determine scheme: use http for localhost/127.0.0.1/0.0.0.0
    is_local = any(x in host.lower() for x in ["localhost", "127.0.0.1", "0.0.0.0"])
    scheme = "http" if is_local else "https"
    
    base = f"{scheme}://{host}"
    logger.debug("Auto-detected base URL: %s", base)
    return base


# =============================
# LOGIN (GOOGLE OAUTH)
# =============================
@rt("/login")
def login(req):
    base_url = get_base_url(req)
    redirect_url = f"{base_url}/auth/callback"
    
    logger.info("Initiating Google OAuth login, redirect: %s", redirect_url)
    
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url,
            }
        })
        
        return RedirectResponse(res.url, status_code=303)
    except Exception as e:
        logger.error("OAuth initiation failed: %s", e)
        return Titled(
            "Login Error",
            P("Failed to initiate login. Please try again."),
            A("Go back", href="/signin")
        )


# =============================
# OAUTH CALLBACK
# =============================
@rt("/auth/callback")
def auth_callback(code: str = "", error: str = ""):
    if error:
        logger.error("OAuth callback error: %s", error)
        return RedirectResponse("/signin?error=auth_failed", status_code=303)
    
    if not code:
        logger.warning("No code provided in callback")
        return RedirectResponse("/signin?error=no_code", status_code=303)
    
    logger.info("Received OAuth callback with code")
    return RedirectResponse(f"/auth/session?code={code}", status_code=303)


# =============================
# SESSION EXCHANGE
# =============================
@rt("/auth/session")
def auth_session(code: str = ""):
    if not code:
        logger.warning("No code in session exchange")
        return RedirectResponse("/signin", status_code=303)

    try:
        # Exchange code for session
        data = supabase.auth.exchange_code_for_session({
            "auth_code": code
        })
        
        if not data or not data.session:
            logger.error("Failed to exchange code for session")
            return RedirectResponse("/signin?error=session_failed", status_code=303)
        
        logger.info("Successfully created session for user: %s", data.user.email)
        
        # Create response with redirect
        resp = Response(
            "",
            status_code=303,
            headers={"Location": "/dashboard"}
        )

        # Set secure cookie
        # Use secure=True only in production (when not localhost)
        is_production = os.getenv("VERCEL_URL") is not None
        
        resp.set_cookie(
            "access_token",
            data.session.access_token,
            httponly=True,
            secure=is_production,  # True in production, False locally
            samesite="Lax",
            path="/",
            max_age=60 * 60 * 24 * 7  # 7 days
        )
        
        # Optional: Also set refresh token
        if data.session.refresh_token:
            resp.set_cookie(
                "refresh_token",
                data.session.refresh_token,
                httponly=True,
                secure=is_production,
                samesite="Lax",
                path="/",
                max_age=60 * 60 * 24 * 30  # 30 days
            )

        return resp
        
    except Exception as e:
        logger.error("Session exchange failed: %s", e)
        return RedirectResponse("/signin?error=exchange_failed", status_code=303)


# =============================
# LOGOUT
# =============================
@rt("/logout")
def logout(req):
    """
    Handle logout - clear cookies and redirect to home
    Works with both regular links and HTMX
    """
    try:
        # Get token from cookie
        token = req.cookies.get("access_token")
        
        # Sign out from Supabase (invalidates token server-side)
        if token:
            try:
                supabase.auth.sign_out()
                logger.info("Signed out from Supabase")
            except Exception as e:
                logger.warning("Supabase sign_out error (ignoring): %s", e)
                # Continue anyway - we'll clear the cookie
        
        logger.info("User logged out")
        
        # Check if this is an HTMX request
        is_htmx = req.headers.get("HX-Request") == "true"
        
        if is_htmx:
            # For HTMX: use HX-Redirect header
            resp = Response(
                "",
                status_code=200,
                headers={"HX-Redirect": "/"}
            )
        else:
            # For regular requests: standard redirect
            resp = RedirectResponse("/", status_code=303)
        
        # Delete both auth cookies
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")
        
        return resp
        
    except Exception as e:
        logger.error("Logout error: %s", e)
        # Even if there's an error, redirect home and clear cookies
        is_htmx = req.headers.get("HX-Request") == "true"
        
        if is_htmx:
            resp = Response("", status_code=200, headers={"HX-Redirect": "/"})
        else:
            resp = RedirectResponse("/", status_code=303)
            
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")
        return resp