from fasthtml.common import *
from dbase.supabase_client import supabase
from inspect import iscoroutinefunction


def require_auth(handler):
    async def wrapper(req):
        token = req.cookies.get("access_token")
        if not token:
            return Redirect("/login")

        user_res = supabase.auth.get_user(token)
        if not user_res or not user_res.user:
            return Redirect("/login")

        req.state.user = user_res.user

        if iscoroutinefunction(handler):
            return await handler(req)
        else:
            return handler(req)

    return wrapper
