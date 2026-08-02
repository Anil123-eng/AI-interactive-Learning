"""User models - profiles, progress, and streaks (Data Layer)."""
from datetime import datetime, date, timedelta

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db


class User(UserMixin, db.Model):
    """Registered learner account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=True)
    avatar_color = db.Column(db.String(20), default="#6366f1")

    # Gamification
    xp = db.Column(db.Integer, default=0, nullable=False, index=True)
    level = db.Column(db.Integer, default=1, nullable=False)
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    longest_streak = db.Column(db.Integer, default=0, nullable=False)
    last_active_date = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    lesson_progress = db.relationship(
        "LessonProgress", back_populates="user", cascade="all, delete-orphan"
    )
    challenge_attempts = db.relationship(
        "ChallengeAttempt", back_populates="user", cascade="all, delete-orphan"
    )
    badges = db.relationship(
        "UserBadge", back_populates="user", cascade="all, delete-orphan"
    )
    activities = db.relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan"
    )

    # ---------- Auth helpers ----------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ---------- Gamification helpers ----------
    def add_xp(self, amount: int) -> bool:
        """Add XP and recompute level. Returns True if the user leveled up."""
        self.xp += amount
        new_level = User.compute_level(self.xp)
        leveled_up = new_level > self.level
        self.level = new_level
        return leveled_up

    @staticmethod
    def compute_level(xp: int) -> int:
        """Level = floor(sqrt(xp / 100)) + 1  (lazy progression)."""
        return int((xp / 100) ** 0.5) + 1

    def update_streak(self, today: date | None = None) -> None:
        """Update daily learning streak based on last active date."""
        today = today or date.today()
        if self.last_active_date == today:
            return  # already counted today
        if self.last_active_date == (today - timedelta(days=1)):
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_active_date = today

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_color": self.avatar_color,
            "xp": self.xp,
            "level": self.level,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
        }

    def __repr__(self):
        return f"<User {self.username}>"


class LessonProgress(db.Model):
    """Tracks completion of a lesson by a user (Data Layer)."""

    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, index=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    xp_earned = db.Column(db.Integer, default=0, nullable=False)

    # Unique constraint: one progress row per (user, lesson)
    __table_args__ = (
        db.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),
    )

    user = db.relationship("User", back_populates="lesson_progress")
    lesson = db.relationship("Lesson", back_populates="progress_records")

    def __repr__(self):
        return f"<LessonProgress user={self.user_id} lesson={self.lesson_id}>"

