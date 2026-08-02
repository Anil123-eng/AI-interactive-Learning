"""Authentication routes - register, login, logout (Presentation Layer)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        display_name = request.form.get("display_name", "")

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html", username=username, email=email, display_name=display_name)

        user, error = AuthService.register(username, email, password, display_name)
        if error:
            flash(error, "danger")
            return render_template("auth/register.html", username=username, email=email, display_name=display_name)

        login_user(user)
        flash(f"Welcome to Hello World with AI, {user.display_name}! 🎉", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "")
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user, error = AuthService.authenticate(identifier, password)
        if error:
            flash(error, "danger")
            return render_template("auth/login.html", identifier=identifier)

        login_user(user, remember=remember)
        next_page = request.args.get("next")
        flash(f"Welcome back, {user.display_name}! 👋", "success")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out. See you soon! 👋", "info")
    return redirect(url_for("main.index"))

