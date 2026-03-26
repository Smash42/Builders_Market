
import base64
from datetime import datetime
from email.message import EmailMessage
import io
import secrets
import hashlib
from datetime import datetime, timedelta
from flask import app, current_app, url_for
import pyotp
import qrcode
from database.connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash




class User:
    def __init__(self, user_id, username, email, password_hash, role = None, permissions = None, mfa_enabled= False, mfa_secret=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.permissions = permissions or []
        self.mfa_enabled = mfa_enabled
        self.mfa_secret = mfa_secret

    
    def CheckPassword(self, password):
        return check_password_hash(self.password_hash, password)
    
    #build user
    @staticmethod
    def _BuildUser(row, db):
        if row is None:
            return None
        
        role = row['role_name']
         #Get Permissions
        permissions = db.execute("""
                                SELECT p.permission_name
                                FROM permissions p
                                JOIN role_permissions rp ON p.permission_id = rp.permission_id
                                JOIN roles r ON r.role_id = rp.role_id
                                WHERE r.role_name = ?
                                     """, (role,)).fetchall()
        permission_list = [p['permission_name'] for p in permissions]

        return User(
                user_id=row['user_id'],
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                role=role,
                permissions=permission_list, 
                mfa_enabled=bool(row['mfa_enabled']),
                mfa_secret=row['mfa_secret']
            )

# Check Email
    @staticmethod
    def FromEmail (email : str):
        db = get_connection()
        try: 
            row = db.execute("""
                             SELECT u.*, r.role_name
                             FROM users u 
                             LEFT JOIN user_roles ur ON u.user_id = ur.user_id 
                             LEFT JOIN roles r ON ur.role_id = r.role_id
                             WHERE u.email = ?
                             """, (email,)).fetchone()

            
            return User._BuildUser(row, db)
        finally:
            db.close()
    
    @staticmethod
    def FromID(user_id : int):
        db = get_connection()
        try:
            row = db.execute("""
                             SELECT u.*, r.role_name
                             FROM users u
                             LEFT JOIN user_roles ur ON u.user_id = ur.user_id
                             LEFT JOIN roles r ON ur.role_id = r.role_id
                             WHERE u.user_id = ?
                             """, (user_id,)).fetchone()
            return User._BuildUser(row, db)
        finally:
            db.close()
    
    
# Create User
    @staticmethod
    def Create(name, email, password):
        db = get_connection()
        try: 
            password_hash = generate_password_hash(password)
            cursor = db.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (name, email, password_hash))
            user_id = cursor.lastrowid

              # Check if first user
            count = db.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
            if count == 4:
                role_id = 1
            else:
                role_id = 3
            #Connect User and Role (default User)
            db.execute("INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)", (user_id, role_id))
            db.commit()

            return User.FromID(user_id)
        
        finally:
            db.close()


    @staticmethod
    def UpdateUser(user_id, name, email):
        db = get_connection()
        try:
            db.execute("""
            UPDATE users
            SET username = ?, email = ?, updated_at = ?
            WHERE user_id = ?
        """, (name, email, datetime.utcnow(), user_id))
            db.commit()
            return User.FromID(user_id)
    
        finally:
            db.close()
            

    #Update Role
    @staticmethod
    def UpdateRole(user_id, role_id):
        db = get_connection()
        try:
            #Delete existing role
            db.execute("""
                       DELETE FROM user_roles
                       WHERE user_id = ?
                       """, (user_id,))

            #Assign role
            db.execute("""
                       INSERT INTO user_roles (user_id, role_id)
                       VALUES (?, ?)
                       """,(user_id, role_id))
            
            db.execute("""
                UPDATE users
                SET  updated_at = ?
                WHERE user_id = ?
                """, (datetime.utcnow(), user_id ))
            
            db.commit()
        finally:
            db.close()


    #Get all Users
    @staticmethod
    def GetAll():
        db= get_connection()
        try:
            rows = db.execute("""
                SELECT u.*, r.role_name
                FROM users u
                LEFT JOIN user_roles ur ON u.user_id = ur.user_id
                LEFT JOIN roles r ON ur.role_id = r.role_id
            """).fetchall()

            users = []
            for row in rows:
                user = User._BuildUser(row, db)
                if user:
                    users.append(user)

            return users
        finally:
            db.close()


    @staticmethod
    def Delete(user_id):
        db = get_connection()
        try:
            db.execute("DELETE FROM user_roles WHERE user_id = ?", (user_id,))
            db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            db.commit()
        finally:
         db.close()

    
    @staticmethod
    def FromUsername (username : str):
        db = get_connection()
        try: 
            row = db.execute("""
                             SELECT u.*, r.role_name
                             FROM users u 
                             LEFT JOIN user_roles ur ON u.user_id = ur.user_id 
                             LEFT JOIN roles r ON ur.role_id = r.role_id
                             WHERE u.username = ?
                             """, (username,)).fetchone()

            
            return User._BuildUser(row, db)
        finally:
            db.close()

    @staticmethod
    def isActive(user_id):
        db = get_connection()
        try: 
            db.execute("""
                            UPDATE users SET is_active = 1 WHERE user_id = ?
                             """, (user_id,))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def isInactive(user_id):
        db = get_connection()
        try: 
            db.execute("""
                            UPDATE users SET is_active = 0 WHERE user_id = ?
                             """, (user_id,))
            db.commit()
        finally:
            db.close()

    #Password Reset Function
    @staticmethod
    def get_reset_token(user_id):
            db = get_connection()
            try: 
                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                expires_at = datetime.utcnow() + timedelta(minutes=3)
                db.execute(""" 
                        INSERT INTO password_reset_tokens (user_id, token_hash, expires_at) VALUES (?, ?, ?)
                           """, (user_id, token_hash, expires_at))
                db.commit()
                return token
            finally:
                db.close()     

    @staticmethod
    def verify_reset_token(token):
        if not token:
            return None
        db = get_connection()
        try: 
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            row = db.execute("""
                             SELECT * FROM password_reset_tokens
                             WHERE token_hash = ? AND used = 0
                             """, (token_hash,)).fetchone()
            
            if not row:
                return None
            
            if datetime.utcnow() > datetime.fromisoformat(row['expires_at']):
                return None
            
            return User.FromID(row['user_id']), row['token_id']
        finally: 
            db.close()

   #Mark token as used         
    @staticmethod
    def UsedToken(token_id):
        db = get_connection()
        try:
            result = db.execute("""
                       UPDATE password_reset_tokens
                       SET used = 1
                       WHERE token_id = ? AND used = 0
                       """, (token_id,))
            db.commit()
            return result.rowcount ==1
        finally:
            db.close()
    
    @staticmethod
    def UpdatePassword(user_id, password):
        db = get_connection()
        try: 
            password_hash = generate_password_hash(password)

            db.execute("""
                       UPDATE users 
                       SET password_hash = ?, updated_at = ?
                       WHERE user_id = ?
                       """, (password_hash, datetime.utcnow(), user_id))
            db.commit()
        finally:
            db.close()
        

    def send_reset_email(user, token):
        app = current_app
        reset_link = url_for('auth.password_reset_confirm', token = token, _external=True)
        
   
        subject= 'Password Reset Request- Builders Market',
        body=f"""To reset your password, visit the following link: 
            {reset_link}
            If you did not make this request, please ignore the email.""",
        
        #logging simulation
        log_entry = f""" [{datetime.utcnow()}]

        TO: {user.email}
        SUBJECT: {subject}
        RESET LINK: {reset_link}
        """
        with open("password_reset.log", "a") as f:
            f.write(log_entry)

        print("[SIMULATED EMAIL SENT, CHECK LOG for password_reset]")

    # 2FA security
    @staticmethod
    def get_2fa_secret():
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code(email, secret):
        url = pyotp.totp.TOTP(secret).provisioning_uri(name = email, issuer_name="Builders Market")

        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format = "PNG")

        return base64.b64encode(buffer.getvalue()).decode()
    
    @staticmethod
    def verify_2fa_code(secret, code):
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window = 1)
    
    @staticmethod
    def enable_2fa(user_id, secret):
        db = get_connection()
        try: 
            db.execute("""
                       UPDATE users
                       SET mfa_secret = ?, mfa_enabled = 1
                       WHERE user_id = ?
                       """, (secret, user_id))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def disable_2fa(user_id):
        db = get_connection()
        try: 
            db.execute("""
                       UPDATE users
                       SET mfa_secret = NULL, mfa_enabled = 0
                       WHERE user_id = ?
                       """, (user_id,))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_backup_codes(user_id, count = 5):
        db = get_connection()
        code = []
        try: 
            for _ in range(count):
                raw = secrets.token_hex(4)
                hashed = hashlib.sha256(raw.encode()).hexdigest()

                db.execute("""
                           INSERT INTO user_backup_codes(user_id, code_hash)
                           VALUES (?, ?)
                           """, (user_id, hashed))
                code.append(raw)

            db.commit()
            return code
        finally:
            db.close()

    @staticmethod
    def verify_backup_codes(user_id, code):
        db = get_connection()
        try:
            hash = hashlib.sha256(code.encode()).hexdigest()

            row = db.execute("""
                             SELECT * FROM user_backup_codes
                             WHERE user_id = ? AND code_hash = ? AND used = 0
                             """, (user_id, hash)).fetchone()
            if not row:
                return False
            db.execute("""
                       UPDATE user_backup_codes
                       SET used = 1
                       WHERE backup_id = ?
                       """, (row['backup_id'],))
            db.commit()

            return True
        finally:
            db.close()
