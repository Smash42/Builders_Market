from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, g, url_for

from models.users import User
from routes.products import products_bp
from routes.carts import carts_bp
from routes.orders import orders_bp
from routes.auth import auth_bp
from routes.categories import category_bp
from routes.reviews import reviews_bp
from routes.admin import admin_bp
from utils.error_handler import register_error_handlers
from database.connection import get_user_by_id

from database.connection import init_db_command


def create_app():
    app = Flask(__name__)

    #Load configuration
    app.config.from_object('config.config.Config')

    app.config['PERMANENT_SESSION_KEY'] = timedelta(hours=24)

    #Register CLI command to initialize DB
    app.cli.add_command(init_db_command)

    register_error_handlers(app)

    @app.before_request
    def current_user():
        user_id = session.get('user_id')
        if user_id:
            user = User.FromID(user_id)
            g.user = user

        else:
            g.user = None
            g.user_permissions = []
            
    @app.before_request
    def require_2fa_for_protected_routes():
        if not request.endpoint:
            return
        
        # Skip auth endpoints
        if request.endpoint.startswith('auth.') or request.endpoint == 'static':
            return
        
        user = getattr(g, 'user', None)
        if not user:
            return
        
        if user and user.mfa_enabled and not session.get('2fa_verified'):
            return redirect(url_for('auth.verify_2fa'))

    @app.route('/')
    def home():
        if g.user is None:
            return render_template('home.html')
        if g.user.role in ["Admin"]:
            return render_template('dashboard_admin.html')
        if g.user.role in ["Moderator"]:
            return render_template('dashboard_mod.html')
        if g.user:
            return render_template('dashboard.html')
        

        # different dashboard for each role? 
        #return render_template('dashboard.html')
            
    
    #register the blueprint so the routes are available to the app
    #Url prefixes are in each .py file 
    app.register_blueprint(products_bp)
    app.register_blueprint(carts_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
