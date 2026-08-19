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
        # Local production: serve only on this computer.
        from waitress import serve

        print("🚀 Serving locally in PRODUCTION mode with Waitress on http://127.0.0.1:5000")
        serve(app, host="127.0.0.1", port=5000, threads=8)
    else:
        # Local development: Flask debug server (autoreload + debugger)
        app.run(debug=True, host="127.0.0.1", port=5000)

