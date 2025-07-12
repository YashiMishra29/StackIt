from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config  # ✅ THIS IS THE FIX

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # ✅ FIXED: now using the actual class directly

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
