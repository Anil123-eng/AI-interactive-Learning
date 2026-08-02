"""Challenge Hub models - coding challenges and attempts (Data Layer)."""
from datetime import datetime

from .. import db


class Challenge(db.Model):
    """A coding challenge with auto-grading test cases."""

    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default="easy", index=True)  # easy/medium/hard
    starter_code = db.Column(db.Text, nullable=False, default="")
    solution_code = db.Column(db.Text, nullable=False)  # reference solution
    test_cases = db.Column(db.JSON, nullable=False)  # list of {input, expected} or raw checks
    hints = db.Column(db.JSON, nullable=True)  # list of hint strings
    xp_reward = db.Column(db.Integer, default=50, nullable=False)
    category = db.Column(db.String(50), default="python", nullable=False)
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    attempts = db.relationship(
        "ChallengeAttempt", back_populates="challenge", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Challenge {self.slug}>"


class ChallengeAttempt(db.Model):
    """A user's attempt at a challenge (Data Layer)."""

    __tablename__ = "challenge_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False, index=True
    )
    code = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, default=False, nullable=False)
    passed_tests = db.Column(db.Integer, default=0, nullable=False)
    total_tests = db.Column(db.Integer, default=0, nullable=False)
    output = db.Column(db.Text, nullable=True)  # captured stdout/stderr
    xp_earned = db.Column(db.Integer, default=0, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="challenge_attempts")
    challenge = db.relationship("Challenge", back_populates="attempts")

    # Composite index for leaderboard / history queries
    __table_args__ = (
        db.Index("ix_attempt_user_challenge", "user_id", "challenge_id"),
    )

    def __repr__(self):
        return f"<ChallengeAttempt user={self.user_id} ch={self.challenge_id} passed={self.passed}>"

