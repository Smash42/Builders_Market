from functools import wraps
from flask import g, jsonify, request



#Decorator to check for Login (authentication)
def login_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        
        #if not g.user:
           #return jsonify({'success': False, 'error': 'Authentication Required. Please log in.'}), 401
        
        #making it a Stub for now to ensure that all routes are working properly. 
        print(f"Authentication required for: {request.path}")  # Debugging statement

        return f(*args, **kwargs)
    return wrapped_view

def user_role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*args, **kwargs):
            # Check if user is logged in and has the required role
            # if not g.user:
            #     return jsonify({'success': False, 'error': 'Authentication Required. Please log in.'}), 401
            # if g.user['role'] != role:
            #     return jsonify({'success': False, 'error': 'Permission Denied. Insufficient role.'}), 403
            
            # Stub for now to ensure that all routes are working properly.
            print(f"Role '{role}' required for: {request.path}")  # Debugging statement

            return f(*args, **kwargs)
        return wrapped_view
    return decorator
#if user.
# Add role for if Admin, then skip permission checks