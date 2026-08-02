"""Challenge Hub routes - list, detail, and submit challenges (Presentation Layer)."""
import json

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..services.challenge_service import ChallengeService

challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("/challenges")
def list_challenges():
    difficulty = request.args.get("difficulty")
    if difficulty not in (None, "easy", "medium", "hard"):
        difficulty = None
    challenges = ChallengeService.get_published_challenges(difficulty=difficulty)
    challenge_data = []
    for challenge in challenges:
        challenge_data.append(
            {
                "challenge": challenge,
                "solved": ChallengeService.is_solved(current_user, challenge),
            }
        )
    return render_template(
        "challenges/list.html",
        challenge_data=challenge_data,
        active_difficulty=difficulty,
    )


@challenges_bp.route("/challenges/<slug>")
def challenge_detail(slug):
    challenge = ChallengeService.get_challenge_by_slug(slug)
    if challenge is None:
        abort(404)
    solved = ChallengeService.is_solved(current_user, challenge)
    best_attempt = ChallengeService.get_user_best_attempt(current_user, challenge)
    return render_template(
        "challenges/detail.html",
        challenge=challenge,
        solved=solved,
        best_attempt=best_attempt,
        test_cases_json=json.dumps(challenge.test_cases),
        hints_json=json.dumps(challenge.hints or []),
    )


@challenges_bp.route("/challenges/<slug>/submit", methods=["POST"])
@login_required
def submit_challenge(slug):
    challenge = ChallengeService.get_challenge_by_slug(slug)
    if challenge is None:
        abort(404)

    code = request.form.get("code", "").strip()
    if not code:
        flash("Please write some code before submitting.", "warning")
        return redirect(url_for("challenges.challenge_detail", slug=challenge.slug))

    result = ChallengeService.grade(current_user, challenge, code)

    # For AJAX submissions, return JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(result)

    if result["passed"]:
        flash(f"Challenge solved! +{result['xp_earned']} XP 🏆", "success")
    else:
        flash(
            f"Not quite — {result['passed_tests']}/{result['total_tests']} tests passed. Keep trying!",
            "warning",
        )
    return redirect(url_for("challenges.challenge_detail", slug=challenge.slug))

