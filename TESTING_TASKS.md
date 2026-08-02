# Step 11: End-to-End Testing & Launch — Task Tracker

- [x] Fix `app/routes/auth.py` — correct template paths to `auth/login.html` / `auth/register.html` (5 occurrences)
- [x] Fix `app/services/challenge_service.py` — `CodeRunner.run_function` must unpack multi-argument test inputs (e.g. `solve(a, b)`)
- [x] Fix `app/services/challenge_service.py` — `grade()` must detect first-time solve BEFORE saving attempt so XP is awarded
- [x] Fix `app/services/challenge_service.py` — add safe `__import__` sandbox so challenge solutions using `import re` work
- [x] Fix `app/models/gamification.py` — add `Badge.to_dict()` so `new_badges` is JSON-serializable
- [x] Make `smoke_test.py` idempotent (clean up leftover test user first)
- [x] Re-run `smoke_test.py` — all endpoints return expected status codes (200), XP/badges verified
- [x] Update `TODO.md` — mark Step 11 complete
- [x] Launch the app (`run.py`) — server running at http://127.0.0.1:5000, all pages verified (200)

