"""Gamification models - badges, user badges, and activity logs (Data Layer)."""
from datetime import datetime

from .. import db


class Badge(db.Model):
    """Achievement badge definition."""

    __tablename__ = "badges"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(20), default="🏅")
    criteria_type = db.Column(db.String(40), nullable=False)
    # e.g. "lessons_completed", "challenges_solved", "total_xp", "streak"
    criteria_value = db.Column(db.Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
        }

    def __repr__(self):
        return f"<Badge {self.slug}>"


class UserBadge(db.Model):
    """Many-to-many between users and badges (earned badges)."""

    __tablename__ = "user_badges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey("badges.id"), nullable=False, index=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )

    user = db.relationship("User", back_populates="badges")
    badge = db.relationship("Badge")

    def __repr__(self):
        return f"<UserBadge user={self.user_id} badge={self.badge_id}>"


class ActivityLog(db.Model):
    """Timeline of user activity for progress tracking."""

    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    activity_type = db.Column(db.String(40), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    xp_earned = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="activities")

    __table_args__ = (
        db.Index("ix_activity_user_created", "user_id", "created_at"),
    )

    def __repr__(self):
        return f"<ActivityLog user={self.user_id} {self.activity_type}>"

