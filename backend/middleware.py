from fasthtml.common import *
from dbase.supabase_client import supabase
from inspect import iscoroutinefunction
import logging

logger = logging.getLogger("middleware")


def require_auth(handler):
    """
    Authentication middleware for protected routes.
    Validates access token and attaches user to request.
    """
    async def wrapper(req):
        # Get token from cookie
        token = req.cookies.get("access_token")
        
        if not token:
            logger.warning("No access token found, redirecting to login")
            return RedirectResponse("/signin", status_code=303)

        try:
            # Verify token and get user
            user_res = supabase.auth.get_user(token)
            
            if not user_res or not user_res.user:
                logger.warning("Invalid token, redirecting to login")
                return RedirectResponse("/signin", status_code=303)
            
            # Attach user to request state
            req.state.user = user_res.user
            
            # Call the actual handler
            if iscoroutinefunction(handler):
                return await handler(req)
            else:
                return handler(req)
                
        except Exception as e:
            logger.error("Auth verification failed: %s", e)
            # Clear invalid cookie and redirect
            resp = RedirectResponse("/signin", status_code=303)
            resp.delete_cookie("access_token", path="/")
            resp.delete_cookie("refresh_token", path="/")
            return resp

    return wrapper


def optional_auth(handler):
    """
    Optional authentication middleware.
    Attaches user to request if authenticated, but doesn't redirect if not.
    Useful for pages that work both logged in and logged out.
    """
    async def wrapper(req):
        token = req.cookies.get("access_token")
        
        if token:
            try:
                user_res = supabase.auth.get_user(token)
                if user_res and user_res.user:
                    req.state.user = user_res.user
                else:
                    req.state.user = None
            except:
                req.state.user = None
        else:
            req.state.user = None
        
        if iscoroutinefunction(handler):
            return await handler(req)
        else:
            return handler(req)

    return wrapper