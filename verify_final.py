"""Final comprehensive verification for the AI Learning Platform.

Runs three suites against the full stack:
  1. CodeRunner unit tests   - every challenge input shape the sandbox must handle
  2. Seed-data integrity     - tutorials / lessons / challenges / badges exist,
                               test cases are well-formed, and reference
                               solutions pass their own test cases
  3. End-to-end flow         - auth, lessons + XP, challenges + XP/badges,
                               playground APIs, progress pages, 404 handler,
                               login guard, logout

Usage:
    python verify_final.py

Exit code 0 = all checks passed, 1 = at least one check failed.
"""
import io
import sys

# Ensure emoji/Unicode in output doesn't crash on Windows (cp1252 console).
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from app import create_app, db
from app.models import Badge, Challenge, Lesson, Tutorial, User
from app.services.challenge_service import CodeRunner

app = create_app()
app.config["WTF_CSRF_ENABLED"] = False

RESULTS = []  # (name, ok, detail)


def check(name, condition, detail=""):
    """Record a single pass/fail check and print it immediately."""
    status = "PASS" if condition else "FAIL"
    RESULTS.append((name, bool(condition), detail))
    print(f"  [{status}] {name}" + (f"  -> {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Suite 1: CodeRunner unit tests
# ---------------------------------------------------------------------------
def code_runner_unit_tests():
    print("\n=== 1. CodeRunner unit tests ===")
    cases = [
        ("multi-arg solve(a, b)", "def solve(a, b):\n    return a + b\n", [3, 4], 7),
        ("single-int arg solve(n)", "def solve(n):\n    return n % 2 == 0\n", 4, True),
        ("string arg solve(s)", "def solve(s):\n    return s[::-1]\n", "hello", "olleh"),
        ("list arg solve(nums)", "def solve(nums):\n    return max(nums)\n", [3, 7, 2, 9], 9),
        (
            "regex import + palindrome",
            'import re\ndef solve(s):\n'
            '    clean = re.sub(r"[^a-zA-Z0-9]", "", s).lower()\n'
            "    return clean == clean[::-1]\n",
            "No 'x' in Nixon",
            True,
        ),
        (
            "fizzbuzz list output",
            'def solve(n):\n'
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            '        if i % 15 == 0:\n            result.append("FizzBuzz")\n'
            '        elif i % 3 == 0:\n            result.append("Fizz")\n'
            '        elif i % 5 == 0:\n            result.append("Buzz")\n'
            "        else:\n            result.append(str(i))\n"
            "    return result\n",
            15,
            ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
             "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"],
        ),
        ("fibonacci nth term", "def solve(n):\n    if n <= 1:\n        return n\n"
         "    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n"
         "    return b\n", 10, 55),
    ]
    for label, code, test_input, expected in cases:
        passed, out, err = CodeRunner.run_function(code, test_input, expected)
        check(label, passed and err is None, err or out[:60])

    # Negative case: code without a function must produce a clean error.
    passed, out, err = CodeRunner.run_function("x = 1\n", 5, 5)
    check("missing function -> clean error", not passed and err is not None, err or "no error raised")

    # Negative case: importing a forbidden module must fail safely.
    passed, out, err = CodeRunner.run_function("import os\ndef solve(n):\n    return n\n", 1, 1)
    check("forbidden import blocked", not passed and err is not None, err or "no error raised")


# ---------------------------------------------------------------------------
# Suite 2: Seed data integrity
# ---------------------------------------------------------------------------
def data_integrity_checks():
    print("\n=== 2. Seed data integrity ===")
    tutorials = Tutorial.query.filter_by(is_published=True).all()
    lessons = Lesson.query.all()
    challenges = Challenge.query.filter_by(is_published=True).all()
    badges = Badge.query.all()

    check("4 tutorials seeded", len(tutorials) == 4, f"found {len(tutorials)}")
    check("12 lessons seeded", len(lessons) == 12, f"found {len(lessons)}")
    check("8 challenges seeded", len(challenges) == 8, f"found {len(challenges)}")
    check("14 badges seeded", len(badges) == 14, f"found {len(badges)}")

    # Every challenge must have a non-empty, well-formed test-case list.
    malformed = []
    for ch in challenges:
        if not isinstance(ch.test_cases, list) or len(ch.test_cases) == 0:
            malformed.append(ch.slug)
            continue
        for case in ch.test_cases:
            if not isinstance(case, dict) or "input" not in case or "expected" not in case:
                malformed.append(ch.slug)
                break
    check("all challenges have well-formed test cases", not malformed,
          "; ".join(malformed) or f"{len(challenges)} challenges OK")

    # Reference solutions must pass their own test cases.
    bad_solutions = []
    for ch in challenges:
        for case in ch.test_cases:
            passed, out, err = CodeRunner.run_function(ch.solution_code, case["input"], case["expected"])
            if not (passed and err is None):
                bad_solutions.append(f"{ch.slug}: {err or 'wrong result'}")
                break
    check("all reference solutions pass their test cases", not bad_solutions,
          "; ".join(bad_solutions) or f"{len(challenges)} solutions OK")


# ---------------------------------------------------------------------------
# Suite 3: End-to-end flow
# ---------------------------------------------------------------------------
def end_to_end_flow():
    print("\n=== 3. End-to-end flow ===")
    client = app.test_client()
    username = "finaltestuser"
    email = "finaltest@example.com"

    # Idempotency: remove a leftover user from a previous run.
    with app.app_context():
        leftover = User.query.filter_by(username=username).first()
        if leftover:
            db.session.delete(leftover)
            db.session.commit()

    # Public pages
    for url in ["/", "/tutorials", "/challenges", "/playground",
                "/auth/login", "/auth/register"]:
        r = client.get(url)
        check(f"GET {url}", r.status_code == 200, f"status={r.status_code}")

    # Login guard: unauthenticated /dashboard redirects to login.
    r = client.get("/dashboard")
    check("dashboard requires login", r.status_code in (301, 302), f"status={r.status_code}")

    # Register a new user (auto-login, redirect to dashboard with welcome flash).
    r = client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": "password123",
            "confirm_password": "password123",
            "display_name": "Final Test User",
        },
        follow_redirects=True,
    )
    check("register + redirect to dashboard", r.status_code == 200 and b"Welcome to Hello World with AI" in r.data,
          f"status={r.status_code}")

    # Authenticated pages
    for url in ["/dashboard", "/progress", "/profile"]:
        r = client.get(url)
        check(f"GET {url} (auth)", r.status_code == 200, f"status={r.status_code}")

    # Tutorial detail + lesson page render
    r = client.get("/tutorials/ai-fundamentals")
    check("GET /tutorials/ai-fundamentals", r.status_code == 200, f"status={r.status_code}")
    r = client.get("/lessons/1")
    check("GET /lessons/1", r.status_code == 200, f"status={r.status_code}")

    # Complete lesson 1 (xp_reward = 20) — XP granted exactly once.
    r = client.post("/lessons/1/complete", follow_redirects=True)
    check("POST complete lesson 1", r.status_code == 200, f"status={r.status_code}")
    with app.app_context():
        u = User.query.filter_by(username=username).first()
        xp_after_lesson = u.xp
    check("lesson XP awarded (20)", xp_after_lesson == 20, f"xp={xp_after_lesson}")

    client.post("/lessons/1/complete", follow_redirects=True)
    with app.app_context():
        u = User.query.filter_by(username=username).first()
        check("no double XP on re-complete", u.xp == xp_after_lesson, f"xp={u.xp}")

    # Challenge detail page
    r = client.get("/challenges/sum-two-numbers")
    check("GET /challenges/sum-two-numbers", r.status_code == 200, f"status={r.status_code}")

    # Submit a correct solution (xp_reward = 30) via AJAX.
    r = client.post(
        "/challenges/sum-two-numbers/submit",
        data={"code": "def solve(a, b):\n    return a + b\n"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    data = r.get_json() or {}
    check("challenge submit -> passed", r.status_code == 200 and data.get("passed"), f"json={data}")
    check("challenge XP earned (30)", data.get("xp_earned") == 30, f"xp_earned={data.get('xp_earned')}")
    with app.app_context():
        u = User.query.filter_by(username=username).first()
        xp_after_challenge = u.xp
    check("XP total after lesson+challenge (50)", xp_after_challenge == 50, f"xp={xp_after_challenge}")

    # Submit the same correct solution again -> already_solved, no double XP.
    r = client.post(
        "/challenges/sum-two-numbers/submit",
        data={"code": "def solve(a, b):\n    return a + b\n"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    data = r.get_json() or {}
    check("repeat submit -> already_solved, no XP",
          data.get("already_solved") is True and data.get("xp_earned") == 0, f"json={data}")

    # Submit a wrong solution -> passed=False, partial tests.
    r = client.post(
        "/challenges/sum-two-numbers/submit",
        data={"code": "def solve(a, b):\n    return a - b\n"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    data = r.get_json() or {}
    check("wrong submit -> passed False",
          data.get("passed") is False and data.get("passed_tests", 0) < data.get("total_tests", 0),
          f"passed={data.get('passed')} tests={data.get('passed_tests')}/{data.get('total_tests')}")

    # Playground APIs
    r = client.post("/playground/chatbot", json={"message": "What is AI?"})
    check("playground chatbot", r.status_code == 200 and "reply" in (r.get_json() or {}), f"status={r.status_code}")
    r = client.post("/playground/sentiment", json={"text": "I love AI!"})
    check("playground sentiment", r.status_code == 200 and "label" in (r.get_json() or {}), f"status={r.status_code}")
    r = client.post("/playground/regression", json={"x": [1, 2, 3], "y": [2, 4, 6]})
    check("playground regression", r.status_code == 200 and "equation" in (r.get_json() or {}), f"status={r.status_code}")
    r = client.post("/playground/perceptron", json={"demo": "and"})
    check("playground perceptron", r.status_code == 200 and "accuracy" in (r.get_json() or {}), f"status={r.status_code}")
    r = client.get("/playground/data")
    check("playground demo data", r.status_code == 200 and "regression" in (r.get_json() or {}), f"status={r.status_code}")

    # Badges awarded for first lesson + first solved challenge.
    with app.app_context():
        u = User.query.filter_by(username=username).first()
        badge_slugs = {ub.badge.slug for ub in u.badges}
    check("badge 'first-steps' earned", "first-steps" in badge_slugs, f"badges={sorted(badge_slugs)}")
    check("badge 'problem-solver' earned", "problem-solver" in badge_slugs, f"badges={sorted(badge_slugs)}")

    # 404 handler
    r = client.get("/this-page-does-not-exist")
    check("404 handler", r.status_code == 404, f"status={r.status_code}")

    # Logout returns to home.
    r = client.get("/auth/logout", follow_redirects=True)
    check("logout -> home", r.status_code == 200, f"status={r.status_code}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 64)
    print(" AI LEARNING PLATFORM — FINAL VERIFICATION")
    print("=" * 64)

    with app.app_context():
        code_runner_unit_tests()
        data_integrity_checks()
    end_to_end_flow()

    print("\n" + "=" * 64)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f" RESULTS: {passed}/{total} checks passed")
    if passed == total:
        print(" ✅ ALL CHECKS PASSED — the platform is ready to launch!")
        return 0

    print(" ❌ SOME CHECKS FAILED:")
    for name, ok, detail in RESULTS:
        if not ok:
            print(f"    FAILED: {name} {detail}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

