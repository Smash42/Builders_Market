from functools import wraps
from flask import g, jsonify, request

# Decorator to check for permissions
def permission_required(permission : str):
    def decorator(f):
        @wraps(f)
        def wrapped_view(*args, **kwargs):
        
            #Check if user has the required permissions here. 
            #Stub for now to ensure all pages are functioning properly
            return f(*args, **kwargs)
        
        return wrapped_view
    return decorator
