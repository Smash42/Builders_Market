from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from auth.auths import login_required
from models.users import User
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

        if len(name) ==0:
            hasError = True
            flash('Error: Enter Valid username')
    
        if len(email) ==0:
            hasError = True
            flash('Error: Enter Valid Email')
    
        if len(password) == 0:
            hasError = True
            flash('Error: Enter Valid Password')

        if len(verifypassword) == 0:
            hasError = True
            flash('Error: Confirm Password')
    
        if password != verifypassword:
            hasError = True
            flash('Error: Passwords do not match')

            #Check Email unique
        if User.FromUsername(name) is not None:
            hasError = True
            flash('Error: Username already registered')
        if hasError:
            return render_template('register.html')
        

    #Check Email unique
        if User.FromEmail(email) is not None:
            hasError = True
            flash('Error: Email already registered')
        if hasError:
            return render_template('register.html')
        

        User.Create(name, email, password)
        flash("User registered successfully")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hasError = False
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()

        if len(email)==0:
            hasError = True
            flash('Error: Enter Valid Email')

        if len(password)==0:
            hasError = True
            flash('Error: Enter a Password')
    
        #Check if Email exits 
        # add From Email to Model users
        user = User.FromEmail(email)

        #Check Password
        if not user or not user.CheckPassword(password):
            #wrong password
            hasError = True
            flash('Error: Login information did not match')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user.user_id
        # if valid, store user info in session to keep them logged in    
        return redirect(url_for('home'))
    
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    flash('User logout successful')
    return redirect(url_for('home'))

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = User.FromID(session['user_id'])
    #Show users profile information, username, email, role, and other relevant information. 
    return render_template('user_profile.html', user=user)

#password reset route
@auth_bp.route('/password-reset', methods=['POST'])
def password_reset():
    #Stub for now to ensure that all routes are working properly.
    #Get email from form, check if email is in DB, if so send password reset instructions to email. 
    flash({'success': True, 'message': 'POST /api/auth/password-reset Route. Password reset instructions sent successfully'}), 200

#password reset confirmation route
@auth_bp.route('/password-reset/confirm', methods=['POST'])
def password_reset_confirm():
    #Stub for now to ensure that all routes are working properly.
    #Get new password and token from form, validate token, if valid update password in DB. 
    flash({'success': True, 'message': 'POST /api/auth/password-reset/confirm Route. Password reset successful'}), 200