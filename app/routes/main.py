"""Main routes - home dashboard (Presentation Layer)."""
from flask import Blueprint, render_template
from flask_login import login_required

from ..services.challenge_service import ChallengeService
from ..services.progress_service import ProgressService
from ..services.tutorial_service import TutorialService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing / home page."""
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Learner dashboard with progress overview."""
    from flask_login import current_user

    tutorials = TutorialService.get_published_tutorials()
    tutorial_progress = [
        {
            **TutorialService.tutorial_progress(current_user, tutorial),
            "tutorial": tutorial,
        }
        for tutorial in tutorials
    ]
    summary = ProgressService.get_user_summary(current_user)
    recent_activity = ProgressService.get_recent_activity(current_user)
    leaderboard = ProgressService.get_leaderboard(limit=5)
    challenge_stats = ChallengeService.get_user_stats(current_user)
    return render_template(
        "dashboard.html",
        tutorials=tutorials,
        tutorial_progress=tutorial_progress,
        summary=summary,
        recent_activity=recent_activity,
        leaderboard=leaderboard,
        challenge_stats=challenge_stats,
    )

