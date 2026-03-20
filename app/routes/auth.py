from datetime import timedelta

from flask import Blueprint, app, flash, redirect, render_template, request, session, url_for
from auth.auths import login_required
from models.users import User
import logging
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
    # from the form get users username, email, password, and verify password.
    ##Check password Meets Requirements!
        hasError = False
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        verifypassword = request.form.get('verifypassword').strip()

        SpecialSymbol = ['!', '@', '#', '$', '?']
        if len(name) ==0:
            hasError = True
            flash('Error: Enter Valid username')
    
        if len(email) ==0:
            hasError = True
            flash('Error: Enter Valid Email')

        if len(verifypassword) == 0:
            hasError = True
            flash('Error: Confirm Password')

        #Check Password Match
        if password != verifypassword:
            hasError = True
            flash('Error: Passwords do not match')

        #Check Email unique
        if User.FromUsername(name) is not None:
            hasError = True
            flash('Error: Username already registered')        

        #Check Email unique
        if User.FromEmail(email) is not None:
            hasError = True
            flash('Error: Email already registered')
        if hasError:
            return render_template('auth/register.html')

        #Check Password Complexity
        if len(password) < 10:
            hasError = True
            flash('Error: Password must be at least 10 characters')
        
        if not any(char.isdigit() for char in password):
            hasError = True
            flash('Error: Password must have at least 1 number')
        
        if not any(char.isupper() for char in password):
            hasError = True
            flash('Error: Password must have at 1 uppercase letter') 

        if not any(char.islower() for char in password):
            hasError = True
            flash('Error: Password must have at least 1 lowercase letter')    

        if not any(char in SpecialSymbol for char in password):
            hasError = True
            flash('Error: Password must have at least 1 Special Character, !@#$?')  

        if hasError:
            return render_template('auth/register.html')

        

        User.Create(name, email, password)
        flash("User registered successfully")
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        hasError = False
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()

        if len(email)==0:
            flash('Error: Enter Valid Email')

        if len(password)==0:
            flash('Error: Enter a Password')
    
        #Check if Email exits 
        user = User.FromEmail(email)

        #Check Password
        if not user or not user.CheckPassword(password):
            #wrong password
            logger.warning(f"Failed Login Attempt for: {email}")
            flash('Error: Login information did not match')
            return render_template('auth/login.html'), 401

        session.clear()
        session['user_id'] = user.user_id
        User.isActive(user.user_id)
        session.permanent = True

        logger.info(f"User {user.user_id} logged in")
        # if valid, store user info in session to keep them logged in    
        return redirect(url_for('home'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    user = User.FromID(session['user_id'])
    User.isInactive(user.user_id)
    session.clear()
    flash('User logout successful')
    return redirect(url_for('home'))

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = User.FromID(session['user_id'])
    #Show users profile information, username, email, role, and other relevant information. 
    return render_template('auth/user_profile.html', user=user)

#password reset route
@auth_bp.route('/password-reset', methods=['GET', 'POST'])
def password_reset():

    if request.method == 'POST':
        email = request.form.get('email').strip()
        user = User.FromEmail(email)

        if user:
            flash('password reset')
            return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html')

#password reset confirmation route
@auth_bp.route('/password-reset/confirm', methods=['GET','POST'])
def password_reset_confirm():
    #Stub for now to ensure that all routes are working properly.
    #Get new password and token from form, validate token, if valid update password in DB. 
    return render_template('auth/password_reset_confirm.html')