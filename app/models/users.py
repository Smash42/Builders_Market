
from datetime import datetime

from database.connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, user_id, username, email, password_hash, role = None, permissions = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.permissions = permissions or []

    
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
                permissions=permission_list
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
        """, (name, email, user_id, datetime.utcnow()))
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