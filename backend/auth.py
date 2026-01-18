from fasthtml.common import *
from main import rt
from dbase.supabase_client import supabase
import os
import logging

logger = logging.getLogger("auth")

# =============================
# BASE URL (RENDER-SAFE)
# =============================
def get_base_url():
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise RuntimeError("BASE_URL is not set")
    return base_url.rstrip("/")


def is_https():
    return get_base_url().startswith("https://")


# =============================
# LOGIN (GOOGLE OAUTH)
# =============================
@rt("/login")
def login(req):
    base_url = get_base_url()
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
            P("Failed to initiate login."),
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

    logger.info("OAuth callback received")
    return RedirectResponse(f"/auth/session?code={code}", status_code=303)


# =============================
# SESSION EXCHANGE
# =============================
@rt("/auth/session")
def auth_session(code: str = ""):
    if not code:
        return RedirectResponse("/signin", status_code=303)

    try:
        data = supabase.auth.exchange_code_for_session({
            "auth_code": code
        })

        if not data or not data.session:
            return RedirectResponse("/signin?error=session_failed", status_code=303)

        logger.info("Session created for %s", data.user.email)

        resp = Response("", status_code=303, headers={"Location": "/dashboard"})

        secure_cookie = is_https()

        resp.set_cookie(
            "access_token",
            data.session.access_token,
            httponly=True,
            secure=secure_cookie,
            samesite="Lax",
            path="/",
            max_age=60 * 60 * 24 * 7,
        )

        if data.session.refresh_token:
            resp.set_cookie(
                "refresh_token",
                data.session.refresh_token,
                httponly=True,
                secure=secure_cookie,
                samesite="Lax",
                path="/",
                max_age=60 * 60 * 24 * 30,
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
    try:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        is_htmx = req.headers.get("HX-Request") == "true"

        if is_htmx:
            resp = Response("", status_code=200, headers={"HX-Redirect": "/"})
        else:
            resp = RedirectResponse("/", status_code=303)

        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")

        return resp

    except Exception as e:
        logger.error("Logout error: %s", e)
        resp = RedirectResponse("/", status_code=303)
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")
        return resp
