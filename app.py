from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    @app.route('/')
    def home():
        return "Welcome to Builders Market!"
    
    @app.route('api/auth/login', methods=['POST'])
    def login():
        return "Login endpoint"

    return app