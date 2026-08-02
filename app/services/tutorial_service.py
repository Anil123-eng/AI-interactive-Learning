"""Tutorial Engine service - lesson progression & completion (Application Layer)."""
from .. import db
from ..models import Lesson, LessonProgress, Tutorial, User
from .gamification_service import GamificationService


class TutorialService:
    """Business rules for the Tutorial Engine."""

    @staticmethod
    def get_published_tutorials():
        """All published tutorials ordered by their sort index."""
        return (
            Tutorial.query.filter_by(is_published=True)
            .order_by(Tutorial.order_index)
            .all()
        )

    @staticmethod
    def get_tutorial_by_slug(slug: str):
        return Tutorial.query.filter_by(slug=slug, is_published=True).first()

    @staticmethod
    def get_lesson_by_id(lesson_id: int):
        return db.session.get(Lesson, lesson_id)

    @staticmethod
    def is_lesson_completed(user: User, lesson: Lesson) -> bool:
        if not user or not user.is_authenticated:
            return False
        return (
            LessonProgress.query.filter_by(user_id=user.id, lesson_id=lesson.id).first()
            is not None
        )

    @staticmethod
    def get_completed_lesson_ids(user: User) -> set[int]:
        if not user or not user.is_authenticated:
            return set()
        rows = LessonProgress.query.filter_by(user_id=user.id).all()
        return {row.lesson_id for row in rows}

    @staticmethod
    def complete_lesson(user: User, lesson: Lesson):
        """Mark a lesson complete, award XP once, and log activity."""
        existing = LessonProgress.query.filter_by(
            user_id=user.id, lesson_id=lesson.id
        ).first()
        if existing:
            return False  # already completed - no double XP

        db.session.add(LessonProgress(user=user, lesson=lesson, xp_earned=lesson.xp_reward))
        GamificationService.award_xp(
            user,
            lesson.xp_reward,
            f"Completed lesson: {lesson.title}",
            "lesson",
        )
        return True

    @staticmethod
    def tutorial_progress(user: User, tutorial: Tutorial) -> dict:
        """Compute progress stats for a tutorial for a given user."""
        lessons = tutorial.lessons
        total = len(lessons)
        if total == 0:
            return {"completed": 0, "total": 0, "percent": 0}

        completed_ids = TutorialService.get_completed_lesson_ids(user)
        completed = sum(1 for lesson in lessons if lesson.id in completed_ids)
        percent = int(round(completed / total * 100))
        return {"completed": completed, "total": total, "percent": percent}

