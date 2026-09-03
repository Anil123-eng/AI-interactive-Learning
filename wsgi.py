"""WSGI entry point for the local Waitress production server.

Usage:
    waitress-serve wsgi:app
"""
from app import create_app

app = create_app("production")

