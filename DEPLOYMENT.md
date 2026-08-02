# 🚀 Deployment Guide — Hello World with AI

This guide covers deploying the **AI Learning Platform** to a cloud host so it
runs 24/7 without depending on your local PC.

---

## Quickest Option: Render (Free)

[Render](https://render.com) offers a free tier with PostgreSQL and automatic
deployments from GitHub. Estimated time: **10 minutes**.

### Step 1 — Push to GitHub

```bash
# From the ai-learning-platform directory
git init
git add .
git commit -m "Initial commit — ready for cloud deploy"
```

Create a **private repository** on GitHub (GitHub > New Repository), then:

```bash
git remote add origin https://github.com/YOUR_USER/ai-learning-platform.git
git push -u origin main
```

### Step 2 — Deploy on Render

1. Go to https://render.com and sign up (GitHub login).
2. Click **New +** → **Blueprint**.
3. Connect your GitHub account and select the `ai-learning-platform` repo.
4. Render will detect the `render.yaml` file in the repo and ask you to confirm:
   - **Web Service**: `ai-learning-platform` (starts automatically)
   - **PostgreSQL Database**: `ai-learning-db` (free tier)
5. Click **Apply** — Render builds and deploys everything.

After ~3 minutes your app is live at `https://ai-learning-platform.onrender.com`.

### Step 3 — Visit your app

The first deploy may take an extra 10 seconds because the database is being
auto-seeded with tutorials, challenges, and badges (set `AUTO_SEED=1`).

---

## Alternative: Railway (Free)

[Railway](https://railway.app) also offers a free tier with PostgreSQL.

1. Install Railway CLI or use the web dashboard.
2. Create a new project → **Deploy from GitHub repo**.
3. Add a **PostgreSQL** database plugin.
4. Set these environment variables:
   - `DATABASE_URL` — *(auto-provided by Railway)*
   - `SECRET_KEY` — generate a random string
   - `AUTO_SEED` — `1`
5. The start command is `gunicorn wsgi:app --bind 0.0.0.0:$PORT`.

---

## Alternative: PythonAnywhere (Free — Limited)

[PythonAnywhere](https://www.pythonanywhere.com) is beginner-friendly.

1. Upload the code or clone from GitHub.
2. Create a **MySQL** database (free tier gives you one).
3. Set up a **manual WSGI file** pointing to `wsgi.py`.
4. Run `python seed.py` manually in a Bash console.
5. Reload the web app.

---

## Environment Variables Reference

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `DATABASE_URL` | Cloud | _(empty)_ | Full connection string (PostgreSQL or MySQL) |
| `SECRET_KEY` | Yes | `dev-secret-key-change-me` | Flask session signing |
| `AUTO_SEED` | No | `0` | Auto-seed DB on first boot (`1` = enabled) |
| `FLASK_DEBUG` | No | `0` | Debug mode (`1` = on, `0` = off) |
| `DB_HOST` | Local | `localhost` | MySQL host |
| `DB_PORT` | Local | `3306` | MySQL port |
| `DB_USER` | Local | `root` | MySQL user |
| `DB_PASSWORD` | Local | _(empty)_ | MySQL password |
| `DB_NAME` | Local | `ai_learning_platform` | MySQL database name |

On cloud hosts, set **only** `DATABASE_URL` and `SECRET_KEY`. The `DB_*`
variables are for local development only.

---

## Maintaining the App

### Updating

```bash
# Make changes locally, then:
git add .
git commit -m "Describe your changes"
git push
```

Render / Railway detect the push and auto-deploy.

### Seeding / Re-seeding

```bash
# Local
cd ai-learning-platform
venv\Scripts\python seed.py

# Cloud (Render shell)
python seed.py
```

### Database backups

The free Render PostgreSQL tier can be backed up via the Render dashboard
(PostgreSQL → Settings → Dump).

---

## Files Included for Deployment

| File | Purpose |
|---|---|
| `wsgi.py` | WSGI entry point for gunicorn/waitress |
| `Procfile` | Render / Railway process definition |
| `runtime.txt` | Python version pin |
| `render.yaml` | Render blueprint (one-click deploy) |
| `.env.example` | Environment variable template |
| `requirements.txt` | All dependencies (gunicorn + waitress + psycopg2) |

---

## Troubleshooting

**App crashes on startup (cloud):**
- Check the logs: `gunicorn` or `waitress` errors.
- Make sure `DATABASE_URL` is set correctly.
- Make sure the database is reachable (Render firewall allows internal connections).

**No tutorials / challenges on first load:**
- Ensure `AUTO_SEED=1` is set in environment variables.
- Or run `python seed.py` manually in the cloud shell.

**Images not loading:**
- Static files are served by Flask in development. For production, use a CDN
  or configure `WHITENOISE` static serving (not needed for this guide).

**500 error on pages:**
- Check the app logs. Common causes: database connection issues, missing
  environment variables, or CSRF token issues (ensure `SECRET_KEY` is set).
