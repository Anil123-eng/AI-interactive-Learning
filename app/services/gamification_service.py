"""Gamification service - XP, badges, streaks, activity (Application Layer)."""
from datetime import datetime

from .. import db
from ..models import ActivityLog, Badge, User, UserBadge


class GamificationService:
    """Business rules for XP, badges, streaks, and activity tracking."""

    # ---------- XP ----------
    @staticmethod
    def award_xp(user: User, amount: int, description: str, activity_type: str = "generic"):
        """Award XP, log activity, update streak, and check for new badges."""
        if amount <= 0:
            return False, []

        leveled_up = user.add_xp(amount)
        user.update_streak()

        db.session.add(
            ActivityLog(
                user=user,
                activity_type=activity_type,
                description=description,
                xp_earned=amount,
            )
        )

        new_badges = GamificationService.check_badges(user)
        db.session.commit()

        return leveled_up, new_badges

    @staticmethod
    def log_activity(user: User, activity_type: str, description: str, xp: int = 0):
        """Append an activity log entry without XP change."""
        db.session.add(
            ActivityLog(
                user=user,
                activity_type=activity_type,
                description=description,
                xp_earned=xp,
            )
        )
        db.session.commit()

    # ---------- Badges ----------
    @staticmethod
    def check_badges(user: User):
        """Evaluate all badge criteria and award any newly earned badges."""
        earned_ids = {ub.badge_id for ub in user.badges}
        newly_awarded = []

        lessons_completed = len(user.lesson_progress)
        challenges_solved = len(
            [a for a in user.challenge_attempts if a.passed]
        )

        for badge in Badge.query.all():
            if badge.id in earned_ids:
                continue
            earned = GamificationService._evaluate_badge(badge, user, lessons_completed, challenges_solved)
            if earned:
                db.session.add(UserBadge(user=user, badge=badge))
                newly_awarded.append(badge)

        return newly_awarded

    @staticmethod
    def _evaluate_badge(badge: Badge, user: User, lessons_completed: int, challenges_solved: int) -> bool:
        """Evaluate a single badge's criteria."""
        value = badge.criteria_value
        if badge.criteria_type == "lessons_completed":
            return lessons_completed >= value
        if badge.criteria_type == "challenges_solved":
            return challenges_solved >= value
        if badge.criteria_type == "total_xp":
            return user.xp >= value
        if badge.criteria_type == "streak":
            return user.current_streak >= value
        if badge.criteria_type == "level":
            return user.level >= value
        if badge.criteria_type == "first_login":
            return True
        return False

