
from functools import wraps
from flask import abort, flash, g, jsonify, redirect, request, url_for



#Decorator to check for Login (authentication)
def login_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        if not g.get("user"): 
           abort(401)
 
        return f(*args, **kwargs)
    return wrapped_view

# Check for role, use in admin.py
def user_role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*arg, **kwargs):
            # Check if user is logged in and has the required role
            if g.user is None:
                flash("Not Authenticated. Please Login")
                abort(401)
            
            user_role = (g.user.role or "").strip().lower()
            allowed_roles = [r.strip().lower() for r in roles]


            if user_role not in allowed_roles:
                abort(403)

            print(f"Role '{roles}' required for: {request.path}")  # Debugging statement

            return f(*arg, **kwargs)
        return wrapped_view
    return decorator
