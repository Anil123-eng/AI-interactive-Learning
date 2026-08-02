"""Tutorial Engine routes - browse courses & complete lessons (Presentation Layer)."""
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..services.tutorial_service import TutorialService

tutorials_bp = Blueprint("tutorials", __name__)


@tutorials_bp.route("/tutorials")
def list_tutorials():
    tutorials = TutorialService.get_published_tutorials()
    tutorial_progress = []
    for tutorial in tutorials:
        tutorial_progress.append(
            {
                **TutorialService.tutorial_progress(current_user, tutorial),
                "tutorial": tutorial,
            }
        )
    return render_template(
        "tutorials/list.html",
        tutorials=tutorials,
        tutorial_progress=tutorial_progress,
    )


@tutorials_bp.route("/tutorials/<slug>")
def tutorial_detail(slug):
    tutorial = TutorialService.get_tutorial_by_slug(slug)
    if tutorial is None:
        abort(404)
    completed_ids = TutorialService.get_completed_lesson_ids(current_user)
    progress = TutorialService.tutorial_progress(current_user, tutorial)
    return render_template(
        "tutorials/detail.html",
        tutorial=tutorial,
        completed_ids=completed_ids,
        progress=progress,
    )


@tutorials_bp.route("/lessons/<int:lesson_id>")
@login_required
def lesson_detail(lesson_id):
    lesson = TutorialService.get_lesson_by_id(lesson_id)
    if lesson is None:
        abort(404)

    tutorial = lesson.tutorial
    is_completed = TutorialService.is_lesson_completed(current_user, lesson)
    completed_ids = TutorialService.get_completed_lesson_ids(current_user)

    # Determine next / previous lesson
    lessons = tutorial.lessons
    idx = next((i for i, l in enumerate(lessons) if l.id == lesson.id), -1)
    prev_lesson = lessons[idx - 1] if idx > 0 else None
    next_lesson = lessons[idx + 1] if idx < len(lessons) - 1 else None

    return render_template(
        "tutorials/lesson.html",
        lesson=lesson,
        tutorial=tutorial,
        is_completed=is_completed,
        completed_ids=completed_ids,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
    )


@tutorials_bp.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    lesson = TutorialService.get_lesson_by_id(lesson_id)
    if lesson is None:
        abort(404)

    was_completed = TutorialService.complete_lesson(current_user, lesson)
    if was_completed:
        flash(f"Lesson completed! +{lesson.xp_reward} XP 🎉", "success")
    else:
        flash("You've already completed this lesson. Keep going!", "info")

    return redirect(url_for("tutorials.lesson_detail", lesson_id=lesson.id))

