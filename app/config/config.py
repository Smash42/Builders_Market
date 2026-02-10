import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    DATABASE = os.path.join(BASE_DIR, 'instance', 'builders_market.db')
    SECRET_KEY = 'dev-secret-key'
