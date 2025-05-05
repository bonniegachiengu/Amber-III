from flask import Flask
from .config import Config, TestingConfig
from .extensions import db, migrate, login_manager, csrf
from . import models


def create_app(config_class=Config, testing=False):
    app = Flask(__name__)

    # If testing is enabled, load the testing configuration
    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import and register blueprints
    from .blueprints.auth import auth_bp
    # from .blueprints.library import library_bp
    # from .blueprints.scrolls import scrolls_bp
    # from .blueprints.player import player_bp
    # from .blueprints.curator import curator_bp
    # from .blueprints.journal import journal_bp
    # from .blueprints.community import community_bp
    # from .blueprints.home import home_bp
    # from .blueprints.api import api_bp
    # from .blueprints.commerce import commerce_bg


    app.register_blueprint(auth_bp)
    # app.register_blueprint(library_bp, url_prefix="/library")
    # app.register_blueprint(scrolls_bp, url_prefix="/scrolls")
    # app.register_blueprint(player_bp, url_prefix="/player")
    # app.register_blueprint(curator_bp, url_prefix="/curator")
    # app.register_blueprint(journal_bp, url_prefix="/journal")
    # app.register_blueprint(community_bp, url_prefix="/hive")
    # app.register_blueprint(home_bp, url_prefix="/")
    # app.register_blueprint(home_bp, url_prefix="/home")
    # app.register_blueprint(api_bp, url_prefix="/api")
    # app.register_blueprint(commerce_bg, url_prefix="/commerce")

    return app
