"""Application entry point.

Usage:
    python run.py              # development (Flask debug server)
    python run.py --prod       # production (Waitress WSGI server)
"""
import os
import sys

from app import create_app

app = create_app()


if __name__ == "__main__":
    if "--prod" in sys.argv or os.getenv("APP_ENV", "").lower() == "production":
        # Production: serve with Waitress (threaded, stable, internet-safe)
        from waitress import serve

        print("🚀 Serving in PRODUCTION mode with Waitress on http://0.0.0.0:5000")
        serve(app, host="0.0.0.0", port=5000, threads=8)
    else:
        # Development: Flask debug server (autoreload + debugger)
        app.run(debug=True, host="0.0.0.0", port=5000)

