from functools import wraps
from flask import abort, g, jsonify, request

# Decorator to check for permissions
def permission_required(permission : str):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*args, **kwargs):

            if not g.user:
                abort(401)
                
            if permission not in g.user.permissions:
                abort(403)

            return f(*args, **kwargs)
        
        return wrapped_view
    return decorator
