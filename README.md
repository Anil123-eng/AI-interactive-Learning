# 🤖 Hello World with AI

> **Interactive AI Learning Platform** — Learn Artificial Intelligence the fun way with structured tutorials, a hands-on AI playground, gamified challenges, and progress tracking.

## 💻 Localhost-only use

This project is configured to run only on your computer at
`http://127.0.0.1:5000`.

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

> The steps below run the app locally on your own machine.

### Prerequisites
- **Python 3.12+**
- **MySQL** (local development)

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
AUTO_SEED=1

# Optional broad mentor answers in the AI Playground
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_API_KEY` is optional. When it is set, EduBot can answer broad mentor
questions through OpenAI. When it is empty, the built-in offline topic chatbot
is used instead. Keep the key only in `.env`; never commit it to GitHub.

### 4. Create the database

```sql
CREATE DATABASE ai_learning_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Seed the data (optional when `AUTO_SEED=1`)

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
├── wsgi.py                  # WSGI entry point (Waitress)
├── seed.py                  # Seed tutorials, challenges, badges
├── Procfile                 # Process definition
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
- **Database:** MySQL (local)
- **Server:** Waitress
- **Frontend:** HTML · CSS · JavaScript (Jinja2 templates)

---

## 📄 License

Built with ❤️ for curious minds. Made for learning and experimentation.

---

This project is intended for localhost-only use.
