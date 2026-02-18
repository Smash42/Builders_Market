
from functools import wraps
from flask import g, jsonify, request



#Decorator to check for Login (authentication)
def login_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        if not g.get("user"): 
           return jsonify({'success': False, 'error': 'Authentication Required. Please log in.'}), 401
 
        return f(*args, **kwargs)
    return wrapped_view

# Check for role, use in admin.py
def user_role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*arg, **kwargs):
            # Check if user is logged in and has the required role
            user = g.get("user")

            if not user:
                return jsonify({'success': False, 'error': 'Authentication Required. Please log in.'}), 401
            
            if user.get("role") not in roles:
                return jsonify({'success': False, 'error': 'Permission Denied. Insufficient role.'}), 403

            print(f"Role '{roles}' required for: {request.path}")  # Debugging statement

            return f(*arg, **kwargs)
        return wrapped_view
    return decorator

