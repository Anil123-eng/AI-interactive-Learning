"""WSGI entry point for production servers (gunicorn, waitress, etc.).

Usage:
    gunicorn wsgi:app          # Linux / cloud hosts
    waitress-serve wsgi:app    # Windows / local production
"""
from app import create_app

app = create_app("production")

