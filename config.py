from base64 import b64encode
import os

uri = os.environ.get("DATABASE_URL", "postgresql:///vibify")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", b64encode(os.urandom(64)).decode("utf-8"))
    CLIENT_ID = "4d550c5919b14f99b85d6347ad6fa9e5"
    CLIENT_SECRET = "c03961d990b3482c96c99b44431a7946"
    REDIRECT_URI = "http://127.0.0.1:5000/callback"
    SCOPE = "user-read-email user-top-read"


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
