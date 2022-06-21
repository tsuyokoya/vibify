from base64 import b64encode
import os

uri = os.environ.get("DATABASE_URL", "postgresql:///vibify")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", b64encode(os.urandom(64)).decode("utf-8"))
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    REDIRECT_URI = os.environ.get("REDIRECT_URI")
    SCOPE = "user-read-email user-top-read user-library-read playlist-modify-private playlist-read-private"


class ProductionConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = uri


class DevelopmentConfig(Config):
    ENV = "development"
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = uri


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql:///vibify-test"
    DEBUG_TB_HOSTS = ["dont-show-debug-toolbar"]
    WTF_CSRF_ENABLED = False
