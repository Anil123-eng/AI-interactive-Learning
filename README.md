# 🤖 Hello World with AI

> **Interactive AI Learning Platform** — Learn Artificial Intelligence the fun way with structured tutorials, a hands-on AI playground, gamified challenges, and progress tracking.

## 🌐 Make It Publicly Accessible on Any Device

> ⚠️ The permanently hosted Render URL was **suspended by its owner**. The fastest way to get the app live on **any device** again is the one-command helper below.

### Option A — One-command public URL (no account needed) ⭐

Run the included helper script to start the app and open a free **Cloudflare Quick Tunnel**:

```bash
python go_public.py
```

This will:
1. Start the app locally (production mode) on `http://localhost:5000`
2. Automatically download `cloudflared.exe` (if missing)
3. Free Cloudflare Quick Tunnel — **no account or login required**
4. Print a public HTTPS URL like `https://<random>.trycloudflare.com`

Open that URL on your **phone, tablet, laptop, or any device** — it works anywhere in the world. Share it with anyone.

> **Note:** The Quick Tunnel URL is temporary — it changes every time you restart `go_public.py`. For a permanent URL, see **Option B** below.

### Option B — Permanent public URL (Render)

The project is fully configured for a permanent deploy on Render (see `render.yaml` and `DEPLOYMENT.md`). Push to GitHub and deploy via Render's Blueprint to get a permanent URL such as `https://<your-service>.onrender.com`.

> The previous deployment was at `https://ai-learning-platform.onrender.com` but was suspended. You can re-create it by redeploying.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 📚 **Tutorial Engine** | Structured lessons covering AI fundamentals, Machine Learning, Neural Networks, and more. |
| 🧪 **AI Playground** | Experiment with a chatbot, sentiment analyzer, linear regression, and a perceptron — live! |
| 🏆 **Challenge Hub** | Solve real coding challenges with auto-grading, earn XP, and climb the leaderboard. |
| 📊 **Progress Tracker** | Track your XP, level, streaks, badges, and weekly learning activity. |
| 🎮 **Gamification** | Earn XP, level up, unlock badges, and build daily streaks as you learn. |

---

## 🚀 Quick Start (Local Development)

> The steps below are for running the app locally on your own machine. To make it public on any device, use `python go_public.py` (see above).

### Prerequisites
- **Python 3.12+**
- **MySQL** (local development) — or set `DATABASE_URL` for PostgreSQL (cloud)

### 1. Set up the virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the environment

Create a `.env` file (or copy `.env.example`). For local **MySQL**:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ai_learning_platform
SECRET_KEY=your-super-secret-key
FLASK_DEBUG=1
```

For **PostgreSQL** (cloud), just set a single var:

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-super-secret-key
```

### 4. Create the database

```sql
CREATE DATABASE ai_learning_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Seed the data (tutorials, challenges, badges)

```bash
python seed.py
```

### 6. Run the app

```bash
# Development (Flask debug server -> http://localhost:5000)
python run.py

# Production (Waitress threaded server -> http://localhost:5000)
python run.py --prod
```

Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🌐 Deploying Your Own Copy (Render)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your GitHub account and select the repo.
4. Render auto-detects `render.yaml` and provisions:
   - **Web Service** (starts automatically)
   - **PostgreSQL Database** (`ai-learning-db`, free tier)
5. Click **Apply** — your app goes live at `https://<your-service>.onrender.com` in ~3 minutes.

> The free tier **auto-seeds** tutorials, challenges, and badges on first boot (`AUTO_SEED=1`), so your app comes up fully populated with zero manual steps.

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for full deploy instructions (Render, Railway, PythonAnywhere).

---

## 🏗️ Project Structure

```
ai-learning-platform/
├── app/
│   ├── __init__.py          # Flask app factory (blueprints, extensions, error handlers)
│   ├── config.py            # Environment-based configuration
│   ├── models/              # Data layer (SQLAlchemy models)
│   │   ├── user.py
│   │   ├── tutorial.py
│   │   ├── challenge.py
│   │   └── gamification.py
│   ├── routes/              # Presentation layer (blueprints)
│   │   ├── main.py          # Home / dashboard
│   │   ├── auth.py          # Register / login / logout
│   │   ├── tutorials.py     # Tutorial engine
│   │   ├── playground.py    # AI playground
│   │   ├── challenges.py    # Challenge hub
│   │   └── progress.py      # Progress & gamification
│   ├── services/            # Application layer (business logic)
│   ├── static/              # CSS / JS / images
│   └── templates/           # Jinja2 HTML templates
├── run.py                   # Entry point (dev / production)
├── wsgi.py                  # WSGI entry point (gunicorn / waitress)
├── seed.py                  # Seed tutorials, challenges, badges
├── render.yaml              # Render one-click blueprint
├── Procfile                 # Render / Railway / Heroku process definition
├── runtime.txt              # Python version pin
└── requirements.txt         # Python dependencies
```

---

## 🧪 Testing & Verification

The project ships with verification scripts:

```bash
python verify_final.py     # 46/46 checks — unit tests, seed integrity, end-to-end flow
python smoke_test.py       # Smoke test all endpoints
python verify_fixes.py     # Verify resolved bugs
```

---

## 🛠️ Environment Variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `DATABASE_URL` | Cloud | _(empty)_ | Full connection string (PostgreSQL / MySQL) |
| `SECRET_KEY` | Yes | `dev-secret-key-change-me` | Flask session signing |
| `AUTO_SEED` | No | `0` | Auto-seed DB on first boot (`1` = enabled) |
| `FLASK_DEBUG` | No | `0` | Debug mode (`1` = on, `0` = off) |
| `DB_HOST` | Local | `localhost` | MySQL host |
| `DB_PORT` | Local | `3306` | MySQL port |
| `DB_USER` | Local | `root` | MySQL user |
| `DB_PASSWORD` | Local | _(empty)_ | MySQL password |
| `DB_NAME` | Local | `ai_learning_platform` | MySQL database name |

---

## 🛡️ Tech Stack

- **Backend:** Python · Flask · Flask-SQLAlchemy · Flask-Login · Flask-WTF
- **Database:** MySQL (local) · PostgreSQL (cloud)
- **Servers:** Waitress (local prod) · Gunicorn (cloud)
- **Frontend:** HTML · CSS · JavaScript (Jinja2 templates)

---

## 📄 License

Built with ❤️ for curious minds. Made for learning and experimentation.

---

🚀 **Make it live on any device: `python go_public.py`**
