from datetime import timedelta

from flask import Blueprint, app, flash, g, redirect, render_template, request, session, url_for
from auth.auths import require_auth
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
            logger.warning(f'Failed Login Attempt for: {email}')
            flash('Error: Login information did not match')
            return render_template('auth/login.html'), 401

        session.clear()
        session['user_id'] = user.user_id

        User.isActive(user.user_id)
        session.permanent = True
        logger.info(f'User {user.user_id} logged in')


        # 2fa verification, optional
        if user.mfa_enabled:
            session['2fa_required'] = True
            return redirect(url_for('auth.verify_2fa'))
        
        #No MFA
        session['2fa_verified'] = True
        # if valid, store user info in session to keep them logged in    
        return redirect(url_for('home'))  
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
@require_auth
def logout():
    user = User.FromID(session['user_id'])
    User.isInactive(user.user_id)
    session.clear()
    flash('User logout successful')
    return redirect(url_for('home'))

@auth_bp.route('/profile', methods=['GET'])
@require_auth
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
            token = User.get_reset_token(user.user_id)
            User.send_reset_email(user, token)
        flash('If the email is valid a password reset has been sent')
        return redirect(url_for('auth.login' ))

    return render_template('auth/password_reset.html')

#password reset confirmation route
@auth_bp.route('/password-reset/confirm/', methods=['GET','POST'])
def password_reset_confirm():

    token = request.args.get('token')

    if request.method == 'POST':
        result = User.verify_reset_token(token)
        
        if result is None:
            flash('This is an invalid or expired token')
            return redirect(url_for('auth.password_reset'))
        
        user, token_id = result
        
        SpecialSymbol = ['!', '@', '#', '$', '?']
 
        password = request.form.get('password').strip()
        confirm = request.form.get('verifypassword').strip()

        if not token or not password:
            flash('Invalid Request')
            return None

        if not User.UsedToken(token_id):
            flash("Token already used or is no longer valid")
            return redirect(url_for('auth.password_reset'))

        if password != confirm:
            flash('Error: Passwords need to match')

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



        User.UpdatePassword(user.user_id, password)
        User.UsedToken(token_id)
        flash('Password Updated Successfully')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset_confirm.html', token = token)



@auth_bp.route('/2fa/setup', methods=['GET', 'POST'])
def setup_2fa():
    user = g.user
    if not user:
        return redirect(url_for('auth.login'))
    
    user = User.FromID(user.user_id)

    if request.method == 'POST':
        token = request.form.get('token')
        secret = session.get('temp_2fa_secret')
        if not secret:
            flash('Setup Session Expired')
            return redirect(url_for('auth.setup_2fa'))
        
        if not User.verify_2fa_code(secret, token):
            flash("Invalid Code")
            return redirect(url_for('auth.setup_2fa'))
        
        User.enable_2fa(user.user_id, secret)
        session.pop('temp_2fa_secret', None)

        codes = User.get_backup_codes(user.user_id) 
        return render_template('auth/2fa_backup_codes.html', codes = codes)

    secret = session.get('temp_2fa_secret')
    if not secret:
        secret = User.get_2fa_secret()
        session['temp_2fa_secret'] = secret

    qr = User.get_qr_code(user.email, secret)
    return render_template('auth/2fa_setup.html', qr_code = qr, secret= secret)


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    user_id = session.get('user_id')

    if not user_id or not session.get('2fa_required'):
        return redirect(url_for('auth.login'))
    
    user = User.FromID(user_id)
    
    if request.method == 'POST':
        token = request.form.get('token')

        if User.verify_2fa_code(user.mfa_secret, token):
            session['2fa_verified'] = True
            session.pop('2fa_required', None)
            flash('2FA Verified. You are now logged in.')
            return redirect(url_for('home'))

        if User.verify_backup_codes(user.user_id, token):
            session['2fa_verified'] = True
            session.pop('2fa_required', None)
            flash('Backup Codes Used')           
            return redirect(url_for('home'))
        
       
        flash('Invalid 2fa Code. Please Try Again')
    
    return render_template('auth/2fa_verify.html')
    

    
@auth_bp.route('/2fa/disable', methods=['GET', 'POST'])
@require_auth
def disable_2fa():
    user = g.user
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':

        password = request.form.get('password')
        token = request.form.get('token')

        if not user.CheckPassword(password):
            flash('Invalid login credentials')
            return redirect(url_for('auth.profile'))
            
        
        if user.mfa_enabled:
            if not User.verify_2fa_code(user.mfa_secret, token):
                flash('Invalid MFA Code')
                return redirect(url_for('auth.profile'))

        User.disable_2fa(user.user_id)

        session.pop('2fa_verified', None)
        flash('2FA Disabled Successfully')
        return redirect(url_for('auth.profile'))
    return render_template('auth/2fa_disable.html')

@auth_bp.route('/2fa/backup-code/regenerate', methods=['GET', 'POST'])
def regen_backup_codes():
    user = g.user
    if not user:
        return redirect(url_for('auth.login'))
    
    codes = User.get_backup_codes(user.user_id) 
    flash("Backup Codes regenerated. Old codes will no longer work")
    return render_template('auth/2fa_backup_codes.html', codes = codes)
    
