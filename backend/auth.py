from fasthtml.common import *
from main import rt
from dbase.supabase_client import supabase


# =============================
# LOGIN (GOOGLE OAUTH)
# =============================
@rt("/login")
def login():
    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "http://localhost:5001/auth/callback",
        }
    })

    return Redirect(res.url)


# =============================
# OAUTH CALLBACK
# =============================
@rt("/auth/callback")
def auth_callback(code: str = ""):
    if not code:
        return Redirect("/login")
    return Redirect(f"/auth/session?code={code}")


# =============================
# SESSION EXCHANGE
# =============================
@rt("/auth/session")
def auth_session(code: str = ""):
    if not code:
        return Redirect("/login")

    data = supabase.auth.exchange_code_for_session({
        "auth_code": code
    })

    resp = Response(
        "",
        status_code=303,
        headers={"Location": "/dashboard"}
    )

    resp.set_cookie(
        "access_token",
        data.session.access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/"
    )

    return resp


# =============================
# LOGOUT
# =============================
@rt("/logout")
def logout():
    resp = Response(
        "",
        status_code=200,
        headers={"HX-Redirect": "/"}
    )
    resp.delete_cookie("access_token", path="/")
    return resp

