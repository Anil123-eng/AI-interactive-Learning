"""Flask application factory for the AI Learning Platform."""
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from .config import config_by_name

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


def create_app(config_name: str = "development") -> Flask:
    """Application factory following the three-layer architecture.

    - Presentation layer: routes/blueprints + templates
    - Application layer: services
    - Data layer: models + repositories
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import & register blueprints (presentation layer)
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.tutorials import tutorials_bp
    from .routes.playground import playground_bp
    from .routes.challenges import challenges_bp
    from .routes.progress import progress_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tutorials_bp)
    app.register_blueprint(playground_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(progress_bp)

    # Import models so SQLAlchemy metadata is populated (data layer)
    from . import models  # noqa: F401

    # Template context processors (available in all templates)
    @app.context_processor
    def inject_globals():
        return {
            "current_user": current_user,
            "app_name": "Hello World with AI",
        }

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # Create tables if they don't exist (dev convenience)
    with app.app_context():
        db.create_all()

        # Optional: auto-seed missing content (AUTO_SEED=1). Each seed function
        # is idempotent, so this also repairs a partially seeded database.
        if app.config.get("AUTO_SEED"):
            from seed import seed_badges, seed_challenges, seed_tutorials

            seed_tutorials()
            seed_challenges()
            seed_badges()
            app.logger.info("Database checked and missing content was seeded.")

    return app


# User loader for Flask-Login
from .models.user import User  # noqa: E402


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

