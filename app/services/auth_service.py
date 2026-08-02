"""Authentication & user management service (Application Layer)."""
from datetime import date

from flask_login import current_user
from werkzeug.security import check_password_hash

from .. import db
from ..models import User
from .gamification_service import GamificationService


class AuthService:
    """Handles registration, login, and user lifecycle business rules."""

    @staticmethod
    def register(username: str, email: str, password: str, display_name: str | None = None):
        """Register a new user. Returns (user, error_message)."""
        username = (username or "").strip()
        email = (email or "").strip().lower()
        display_name = (display_name or "").strip() or username

        # Validation
        if len(username) < 3:
            return None, "Username must be at least 3 characters."
        if len(password) < 6:
            return None, "Password must be at least 6 characters."
        if User.query.filter_by(username=username).first():
            return None, "Username is already taken."
        if User.query.filter_by(email=email).first():
            return None, "An account with that email already exists."

        user = User(
            username=username,
            email=email,
            display_name=display_name,
            avatar_color="#6366f1",
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Welcome activity + initial badge
        GamificationService.log_activity(
            user, "account", "Welcome to Hello World with AI! 🎉", 0
        )

        return user, None

    @staticmethod
    def authenticate(identifier: str, password: str):
        """Authenticate by username or email. Returns (user, error)."""
        identifier = (identifier or "").strip()
        if not identifier or not password:
            return None, "Please enter your username/email and password."

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(password):
            return None, "Invalid credentials. Please try again."

        # Update streak on login
        user.update_streak()
        db.session.commit()
        return user, None

    @staticmethod
    def get_leaderboard(limit: int = 10):
        """Top learners by XP (optimized with index on xp)."""
        return (
            User.query.order_by(User.xp.desc(), User.level.desc())
            .limit(limit)
            .all()
        )

