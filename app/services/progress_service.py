"""Progress Tracker service - dashboards & analytics (Application Layer)."""
from datetime import datetime, timedelta

from sqlalchemy import func

from .. import db
from ..models import ActivityLog, ChallengeAttempt, Lesson, LessonProgress, Tutorial, User


class ProgressService:
    """Aggregates learning progress for the Progress Tracker module."""

    @staticmethod
    def get_user_summary(user: User) -> dict:
        """Overall progress snapshot for the dashboard."""
        total_lessons = Lesson.query.count()
        completed_lessons = (
            LessonProgress.query.filter_by(user_id=user.id).count()
            if user and user.is_authenticated
            else 0
        )
        tutorials = Tutorial.query.filter_by(is_published=True).all()
        tutorial_data = []
        for tutorial in tutorials:
            completed_ids = set()
            if user and user.is_authenticated:
                completed_ids = set(
                    row.lesson_id
                    for row in LessonProgress.query.filter_by(user_id=user.id).all()
                    if row.lesson_id
                )
            total = len(tutorial.lessons)
            completed = sum(1 for lesson in tutorial.lessons if lesson.id in completed_ids)
            tutorial_data.append(
                {
                    "tutorial": tutorial,
                    "completed": completed,
                    "total": total,
                    "percent": int(round(completed / total * 100)) if total else 0,
                }
            )

        stats = ChallengeServiceStats.stats(user)
        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "tutorial_data": tutorial_data,
            "challenges_solved": stats["solved"],
            "challenges_attempted": stats["attempted"],
            "badges_count": len(user.badges) if user and user.is_authenticated else 0,
            "xp": user.xp if user and user.is_authenticated else 0,
            "level": user.level if user and user.is_authenticated else 1,
            "streak": user.current_streak if user and user.is_authenticated else 0,
            "longest_streak": user.longest_streak if user and user.is_authenticated else 0,
        }

    @staticmethod
    def get_recent_activity(user: User, limit: int = 8):
        if not user or not user.is_authenticated:
            return []
        return (
            ActivityLog.query.filter_by(user_id=user.id)
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_activity_chart(user: User, days: int = 14):
        """XP earned per day for the last N days (for charts)."""
        if not user or not user.is_authenticated:
            return []
        since = datetime.utcnow() - timedelta(days=days)
        rows = (
            db.session.query(
                func.date(ActivityLog.created_at).label("day"),
                func.sum(ActivityLog.xp_earned).label("xp"),
            )
            .filter(
                ActivityLog.user_id == user.id,
                ActivityLog.created_at >= since,
                ActivityLog.xp_earned > 0,
            )
            .group_by(func.date(ActivityLog.created_at))
            .order_by(func.date(ActivityLog.created_at))
            .all()
        )
        return [{"day": str(row.day), "xp": int(row.xp or 0)} for row in rows]

    @staticmethod
    def get_leaderboard(limit: int = 10):
        """Global leaderboard sorted by XP."""
        return (
            User.query.order_by(User.xp.desc(), User.level.desc(), User.username.asc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_user_rank(user: User) -> int:
        """1-based rank of a user by XP."""
        if not user or not user.is_authenticated:
            return 0
        higher = User.query.filter(User.xp > user.xp).count()
        return higher + 1


# Small helper to avoid circular imports with ChallengeService
class ChallengeServiceStats:
    @staticmethod
    def stats(user: User) -> dict:
        if not user or not user.is_authenticated:
            return {"solved": 0, "attempted": 0}
        attempts = ChallengeAttempt.query.filter_by(user_id=user.id).all()
        solved = sum(1 for a in attempts if a.passed)
        return {"solved": solved, "attempted": len(attempts)}

