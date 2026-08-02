"""End-to-end smoke test for the AI Learning Platform."""
from app import create_app, db
from app.models import User

app = create_app()
app.config["WTF_CSRF_ENABLED"] = False

# Idempotency: remove any leftover test user from a previous run so the
# registration step below always succeeds and XP assertions are clean.
# Use the ORM so cascade="all, delete-orphan" cleans up dependent rows.
with app.app_context():
    leftover = User.query.filter_by(username="testuser").first()
    if leftover:
        db.session.delete(leftover)
        db.session.commit()

with app.test_client() as client:
    # Public pages
    for url in ["/", "/tutorials", "/challenges", "/playground", "/auth/login", "/auth/register"]:
        r = client.get(url)
        print(f"{url} -> {r.status_code}")

    # Register a user
    r = client.post(
        "/auth/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "display_name": "Test User",
        },
        follow_redirects=True,
    )
    print(f"register -> {r.status_code}")

    # Authenticated pages
    for url in ["/dashboard", "/progress", "/profile"]:
        r = client.get(url)
        print(f"{url} (auth) -> {r.status_code}")

    # Tutorial detail + lesson
    r = client.get("/tutorials/ai-fundamentals")
    print(f"/tutorials/ai-fundamentals -> {r.status_code}")
    r = client.get("/lessons/1")
    print(f"/lessons/1 -> {r.status_code}")

    # Complete a lesson
    r = client.post("/lessons/1/complete", follow_redirects=True)
    print(f"complete lesson -> {r.status_code}")

    # Challenge detail + submit correct solution
    r = client.get("/challenges/sum-two-numbers")
    print(f"/challenges/sum-two-numbers -> {r.status_code}")
    r = client.post(
        "/challenges/sum-two-numbers/submit",
        data={"code": "def solve(a, b):\n    return a + b\n"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    print(f"submit challenge -> {r.status_code} {r.get_json()}")

    # Playground endpoints
    r = client.post("/playground/chatbot", json={"message": "What is AI?"})
    print(f"chatbot -> {r.status_code} reply={r.get_json()['reply'][:40]!r}")
    r = client.post("/playground/sentiment", json={"text": "I love AI!"})
    print(f"sentiment -> {r.status_code} {r.get_json()['label']}")
    r = client.post("/playground/regression", json={"x": [1, 2, 3], "y": [2, 4, 6]})
    print(f"regression -> {r.status_code} {r.get_json()['equation']}")
    r = client.post("/playground/perceptron", json={"demo": "and"})
    print(f"perceptron -> {r.status_code} acc={r.get_json()['accuracy']}")

    # Logout
    r = client.get("/auth/logout", follow_redirects=True)
    print(f"logout -> {r.status_code}")

    # Check user got XP for lesson + challenge
    with app.app_context():
        u = User.query.filter_by(username="testuser").first()
        print(f"User XP: {u.xp}, Level: {u.level}, Streak: {u.current_streak}")
        print(f"Badges: {[ub.badge.slug for ub in u.badges]}")

