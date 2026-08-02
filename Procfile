# Render / Railway / Heroku process definition
# AUTO_SEED=1 in the environment makes a fresh database come up fully populated.
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120

