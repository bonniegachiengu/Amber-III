from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, csrf
from . import models


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import and register blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.library import library_bp
    from .blueprints.scrolls import scrolls_bp
    from .blueprints.player import player_bp
    from .blueprints.curator import curator_bp
    from .blueprints.journal import journal_bp
    from .blueprints.community import community_bp
    from .blueprints.home import home_bp
    from .blueprints.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(scrolls_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(curator_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
