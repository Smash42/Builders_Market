import functools
from flask import Blueprint, g, jsonify


bp=Blueprint('auth', __name__)

#Decorator to check for Login (authentication)
def login_required(f):
    @functools.wraps(f)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return jsonify({'error': 'Authentication Required. Please log in.'}), 401
        return f(*args, **kwargs)
    return wrapped_view

