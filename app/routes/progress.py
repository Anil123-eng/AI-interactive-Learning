"""Progress Tracker routes - dashboard, leaderboard, profile (Presentation Layer)."""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..services.gamification_service import GamificationService
from ..services.progress_service import ProgressService

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/progress")
@login_required
def overview():
    """Full progress tracker page."""
    summary = ProgressService.get_user_summary(current_user)
    recent_activity = ProgressService.get_recent_activity(current_user, limit=12)
    activity_chart = ProgressService.get_activity_chart(current_user, days=14)
    leaderboard = ProgressService.get_leaderboard(limit=10)
    rank = ProgressService.get_user_rank(current_user)
    return render_template(
        "progress/overview.html",
        summary=summary,
        recent_activity=recent_activity,
        activity_chart=activity_chart,
        leaderboard=leaderboard,
        rank=rank,
    )


@progress_bp.route("/profile")
@login_required
def profile():
    """User profile with badges, stats, and recent achievements."""
    summary = ProgressService.get_user_summary(current_user)
    badges = sorted(current_user.badges, key=lambda ub: ub.earned_at, reverse=True)
    recent_activity = ProgressService.get_recent_activity(current_user, limit=8)
    return render_template(
        "progress/profile.html",
        summary=summary,
        badges=badges,
        recent_activity=recent_activity,
    )

