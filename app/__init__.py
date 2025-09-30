import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    
    from .routes import api_bp
    app.register_blueprint(api_bp,url_prefix="/api")
    
    # Import all models of the file
    from . import models
    
    
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    return app
    
    
