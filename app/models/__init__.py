"""Data Layer - SQLAlchemy models.

Import all model modules so SQLAlchemy metadata is populated when
create_all() is called from the application factory.
"""
from .user import User, LessonProgress  # noqa: F401
from .tutorial import Tutorial, Lesson  # noqa: F401
from .challenge import Challenge, ChallengeAttempt  # noqa: F401
from .gamification import Badge, UserBadge, ActivityLog  # noqa: F401

