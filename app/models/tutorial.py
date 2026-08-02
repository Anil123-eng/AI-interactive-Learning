"""Tutorial Engine models - tutorials and lessons (Data Layer)."""
from datetime import datetime

from .. import db


class Tutorial(db.Model):
    """A structured course containing ordered lessons."""

    __tablename__ = "tutorials"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default="🤖")  # emoji icon
    color = db.Column(db.String(20), default="#6366f1")
    difficulty = db.Column(db.String(20), default="beginner")  # beginner/intermediate/advanced
    order_index = db.Column(db.Integer, default=0, nullable=False)
    estimated_minutes = db.Column(db.Integer, default=10, nullable=False)
    is_published = db.Column(db.Boolean, default=True, nullable=False)

    lessons = db.relationship(
        "Lesson",
        back_populates="tutorial",
        order_by="Lesson.order_index",
        cascade="all, delete-orphan",
    )

    @property
    def lesson_count(self):
        return len(self.lessons)

    def __repr__(self):
        return f"<Tutorial {self.slug}>"


class Lesson(db.Model):
    """A single lesson within a tutorial."""

    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    tutorial_id = db.Column(
        db.Integer, db.ForeignKey("tutorials.id"), nullable=False, index=True
    )
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)  # HTML content
    order_index = db.Column(db.Integer, default=0, nullable=False)
    estimated_minutes = db.Column(db.Integer, default=5, nullable=False)
    xp_reward = db.Column(db.Integer, default=20, nullable=False)

    # Unique constraint: one lesson per slug per tutorial
    __table_args__ = (
        db.UniqueConstraint("tutorial_id", "slug", name="uq_tutorial_lesson_slug"),
    )

    tutorial = db.relationship("Tutorial", back_populates="lessons")
    progress_records = db.relationship(
        "LessonProgress", back_populates="lesson", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Lesson {self.title}>"

