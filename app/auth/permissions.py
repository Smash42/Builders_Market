from functools import wraps
from flask import g, jsonify, request

# Decorator to check for permissions
def permission_required(permission : str):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*args, **kwargs):
            if permission not in g.user.get("permissions", []):
                return jsonify({"success": False, "error": "Forbidden"}), 403

            return f(*args, **kwargs)
        
        return wrapped_view
    return decorator
