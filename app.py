import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # WSGI middleware for proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        
        # Create admin user if it doesn't exist
        from models import User
        from werkzeug.security import generate_password_hash
        
        admin_email = "brunabarbozasofia@gmail.com"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            admin = User(
                name="Bruna Barboza",
                email=admin_email,
                password_hash=generate_password_hash("Escola00"),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            logging.info(f"Admin user created: {admin_email}")
    
    # Context processor for global template variables
    @app.context_processor
    def inject_global_vars():
        from datetime import datetime
        return {
            'current_year': datetime.now().year
        }
    
    # Register blueprints
    from routes import main_bp, auth_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

# Create the app instance
app = create_app()
