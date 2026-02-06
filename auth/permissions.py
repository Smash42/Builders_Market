import functools
from flask import g, jsonify


# Decorator to check for permissions
def permission_required(permission : str):
    def decorator(f):
        @functools.wraps(f)
        def wrapped_view(*args, **kwargs):
            if not g.user:
                return jsonify({'error': 'Authentication Required. Please log in. '}), 401           
            if not g.user.has_permission(permission):
                return jsonify({'error': 'You do not have permission to access this page.'}), 403
            return f(*args, **kwargs)
        return wrapped_view
    return decorator
