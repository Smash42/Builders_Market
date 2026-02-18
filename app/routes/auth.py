from flask import Blueprint, request, jsonify, session
from auth.auths import login_required
from models.users import User
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # from the form get users username, email, password, and verify password.
    ##Check password Meets Requirements!
    hasError = False
    name = request.form['name'].strip()
    if len(name) ==0:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Enter Valid username'}), 400
    
    email = request.form['email'].strip()
    if len(email) ==0:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Enter Valid Email'}), 400
    
    password = request.form['password'].strip()
    if len(password) == 0:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Enter Valid Password'}), 400
    verifypassword = request.form['verifypassword'].strip()
    if len(verifypassword) == 0:
            hasError = True
            return jsonify({'success': False, 'message': 'Error: Confirm Password'}), 400
    
    if password != verifypassword:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Passwords do not match'}), 400
    
    #Check Email unique
    check = User.FromEmail(email)
    if check != None:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Email already registered'}), 400
    

    # Ensure username and email is unique, and password and verify password match.
    # Hash the password and store the user in the database with default role of 'user'
    if not hasError:
        user = User.Create(name, email, password)
    return jsonify({'success': True, 'message': 'POST /api/auth/register Route. User registration successful'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email'].strip()
    if len(email)==0:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Enter Valid Email'}), 400
    password = request.form['password'].strip()
    if len(password)==0:
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Enter a Password'}), 400
    
    #Check if Email exits 
    # add From Email to Model users
    user = User.FromEmail(email)
    if user == None:
        #no email found
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Login information did not match'}), 400
    #Check Password
    from werkzeug.security import check_password_hash
    if user.CheckPassword(password) ==False:
        #wrong password
        hasError = True
        return jsonify({'success': False, 'message': 'Error: Login information did not match'}), 400

    session['userid'] = user.user_id
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