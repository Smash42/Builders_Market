from flask import Blueprint, request, jsonify, session
from auth.auths import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    #Stub for now to ensure that all routes are working properly.
    # from the form get users username, email, password, and verify password.
    # Ensure username and email is unique, and password and verify password match.
    # Hash the password and store the user in the database with default role of 'user'
    return jsonify({'success': True, 'message': 'POST /api/auth/register Route. User registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    #Stub for now to ensure that all routes are working properly.
    #Check for username to be found in DB
    # check password against matching username in DB
    # if valid, store user info in session to keep them logged in
    return jsonify({'success': True, 'message': 'POST /api/auth/login Route. User login successful'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'POST /api/auth/logout Route. User logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    #Show users profile information, username, email, role, and other relevant information. 
    return jsonify({'success': True, 'message': 'GET /api/auth/profile Route. User profile retrieved successfully'}), 200

#password reset route
@auth_bp.route('/password-reset', methods=['POST'])
def password_reset():
    #Stub for now to ensure that all routes are working properly.
    #Get email from form, check if email is in DB, if so send password reset instructions to email. 
    return jsonify({'success': True, 'message': 'POST /api/auth/password-reset Route. Password reset instructions sent successfully'}), 200

#password reset confirmation route
@auth_bp.route('/password-reset/confirm', methods=['POST'])
def password_reset_confirm():
    #Stub for now to ensure that all routes are working properly.
    #Get new password and token from form, validate token, if valid update password in DB. 
    return jsonify({'success': True, 'message': 'POST /api/auth/password-reset/confirm Route. Password reset successful'}), 200