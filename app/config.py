"""Application configuration - reads from environment variables (.env file)."""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration for the AI Learning Platform."""

    # Flask core
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = False

    # Local MySQL database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "ai_learning_platform")

    # URL-encode password so special characters (@, #, etc.) don't break the URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Keep the local pool small and recycle connections periodically.
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 120,
        "pool_pre_ping": True,
    }
    # Auto-seed tutorials/challenges/badges when the database is empty (AUTO_SEED=1).
    # Lets a fresh local database come up fully populated with zero manual steps.
    AUTO_SEED = os.getenv("AUTO_SEED", "0") == "1"

    # Session & security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7 days

    # Gamification constants
    XP_PER_LESSON = 20
    XP_PER_CHALLENGE_BASE = 50
    XP_CHALLENGE_BONUS = {"easy": 0, "medium": 25, "hard": 60}
    STREAK_DAILY_BONUS = 10


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # In production, prefer environment-provided secret
    SECRET_KEY = os.getenv("SECRET_KEY", "must-set-in-production")


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

