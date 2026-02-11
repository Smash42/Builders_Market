import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'builder_db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}