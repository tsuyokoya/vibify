import logging

from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from app.extensions import db, connect_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Initialize Flask extensions here
    debug = DebugToolbarExtension(app)
    migrate = Migrate(app, db, compare_type=True)
    connect_db(app)
    logging.basicConfig(
        filename="logs.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s : %(message)s",
    )

    # Register blueprints here
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.authentication import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.playlist import bp as playlist_bp

    app.register_blueprint(playlist_bp, url_prefix="/playlist")

    return app
