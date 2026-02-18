from flask import g
from database.connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

# move get user by id, or get all users to here?
class User:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.email = None
        self.password_hash = None
        self.role = None
    
    def CheckPassword(self, password):
        return check_password_hash(self.password_hash, password)

# Check Email
    @staticmethod
    def FromEmail (email : str):
        db = get_connection()
        sql = "SELECT * FROM users WHERE email = ?;"
        result = db.execute(sql, [email]).fetchone()
        return User.FromDBRow(result)
    
# Create User
    @staticmethod
    def Create(name, email, password):
        db = get_connection()
        sql = """INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?);"""
        cursor = db.execute(sql, [name, email, generate_password_hash(password)])
        id = cursor.lastrowid
        db.commit()
        return User.FromDB(id)

    @staticmethod
    def FromDBRow(row):
        if row is None:
            return None
        out = User()
        out.user_id = row['user_id']
        out.username = row['username']
        out.email = row['email']
        out.password_hash = row['password_hash']
        out.role = row['role']
        return out 
    
    @staticmethod
    def FromDB(id : int):
        db = get_connection()
        sql = "SELECT * FROM users WHERE user_id = ?;"
        result = db.execute(sql, [id]).fetchone()
        return User.FromDBRow(result)
    
