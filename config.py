"""config.py"""

from dotenv import load_dotenv
import os

load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.environ.get("SECRET_KEY", "app_secret_key")
    SECRET_KEY = "a_very_secret_and_long_dev_key_123456789"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    SESSION_COOKIE_SECURE = True


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or \
        f"sqlite:///{os.path.join(basedir, 'dev.db')}"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or \
        "sqlite:///:memory:"
    BCRYPT_LOG_ROUNDS = 4  # Faster hashing for tests


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SESSION_COOKIE_SECURE = True  # Only over HTTPS in production
