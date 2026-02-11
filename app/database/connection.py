import os
import sqlite3

import click
from config.config import Config
from sqlite3 import Error
from flask import g

    
#Database Connection function with error handling
def get_connection():
    try:
        conn = sqlite3.connect(Config.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn  
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Run SQL file to create tables
def initialize_database(): 
    db = get_connection()
    if db is not None:
        try:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r') as f:
                db.executescript(f.read())    
            print("Database initialized successfully.")     

        except FileNotFoundError:
            print("Error: schema.sql file not found!")
        except Error as e:
            print(f"Error executing schema.sql: {e}")
        finally:
            db.commit()
            db.close()

# Query get user by ID  
def get_user_by_id(user_id):
    db = get_connection()
    if db is not None:
        try:
            query = """SELECT user_id, username, email, created_at FROM users WHERE user_id = ?"""
            return db.execute(query, (user_id,)).fetchone()
        except Error as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            db.close()


#View all users, for Admin
def get_all_users():
    db = get_connection()
    if db:
        try:
            query = """SELECT user_id, username, email, created_at FROM users"""
            return db.execute(query).fetchall()
        except Error as e:
            print(f"Error fetching users: {e}")
            return None
        finally:
            db.close()


#Query function category ID         
def get_category_by_id(category_id):
    db = get_connection()
    if db:
        try:            
            query = """SELECT category_id FROM categories WHERE category_id = ?"""
            return db.execute(query, (category_id,)).fetchone()
        except Error as e:
            print(f"Error fetching category: {e}")
            return None
        finally:
            db.close()
          
            
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    initialize_database()
    click.echo('Initialized the database.')