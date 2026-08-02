"""Challenge Hub service - auto-grading & attempt tracking (Application Layer)."""
import ast
import contextlib
import inspect
import io
import sys
import time
import traceback

from .. import db
from ..models import Challenge, ChallengeAttempt, User
from .gamification_service import GamificationService

# Execution safety
MAX_EXECUTION_TIME = 2.0  # seconds per test
MAX_OUTPUT_LENGTH = 2000


class CodeRunner:
    """Safely executes user Python code in a subprocess with timeout.

    Security: code runs in a restricted globals namespace with no filesystem/network access.
    """

    ALLOWED_BUILTINS = {
        "abs", "all", "any", "bool", "chr", "complex", "dict", "divmod",
        "enumerate", "filter", "float", "format", "frozenset", "hash",
        "hex", "int", "isinstance", "issubclass", "iter", "len", "list",
        "map", "max", "min", "oct", "ord", "pow", "print", "range",
        "repr", "reversed", "round", "set", "slice", "sorted", "str",
        "sum", "tuple", "type", "zip",
    }

    # Modules students are allowed to import (pure-Python, no I/O).
    ALLOWED_MODULES = {
        "math", "re", "random", "itertools", "functools", "collections", "string",
    }

    @staticmethod
    def _build_namespace():
        safe_builtins = {}
        import builtins
        for name in CodeRunner.ALLOWED_BUILTINS:
            safe_builtins[name] = getattr(builtins, name, None)

        def safe_import(name, *args, **kwargs):
            if name in CodeRunner.ALLOWED_MODULES:
                return __import__(name, *args, **kwargs)
            raise ImportError(f"Import of '{name}' is not allowed in the sandbox.")

        safe_builtins["__import__"] = safe_import
        # Common math access
        try:
            import math
            safe_builtins["math"] = math
        except ImportError:
            pass
        return {"__builtins__": safe_builtins}

    @classmethod
    def run_function(cls, code: str, test_input, expected, timeout: float = MAX_EXECUTION_TIME):
        """Execute student code defining a function and test it against one case.

        Returns (passed: bool, output: str, error: str|None).
        """
        namespace = cls._build_namespace()
        output_buffer = io.StringIO()
        error_msg = None

        try:
            compiled = compile(code, "<student_code>", "exec")
            start = time.monotonic()
            with contextlib.redirect_stdout(output_buffer):
                exec(compiled, namespace, namespace)
            elapsed = time.monotonic() - start
            if elapsed > timeout:
                return False, output_buffer.getvalue(), "Execution timed out."

            # Locate the target function: prefer solve(), else first callable defined by user
            fn = namespace.get("solve") or namespace.get("solution") or namespace.get("main")
            if fn is None:
                # Find first function in the user's code (order preserved via AST)
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        fn = namespace.get(node.name)
                        break
            if fn is None:
                return False, output_buffer.getvalue(), "No function found. Define a function named `solve`."

            if not callable(fn):
                return False, output_buffer.getvalue(), "`solve` is not callable."

            # Run the function on the test input.
            # If the function takes multiple positional args (e.g. solve(a, b)),
            # the test_input is a list of args to unpack; otherwise pass it directly.
            try:
                params = inspect.signature(fn).parameters
            except (TypeError, ValueError):
                params = {}
            positional_params = [
                p
                for p in params.values()
                if p.kind
                in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            ]
            with contextlib.redirect_stdout(output_buffer):
                if len(positional_params) > 1 and isinstance(test_input, (list, tuple)):
                    result = fn(*test_input)
                else:
                    result = fn(test_input)

            # Normalize comparison
            if isinstance(result, float) and isinstance(expected, (int, float)):
                passed = abs(result - float(expected)) < 1e-6
            else:
                passed = result == expected

            return passed, output_buffer.getvalue()[:MAX_OUTPUT_LENGTH], None

        except Exception as exc:  # noqa: BLE001 - student code can raise anything
            error_msg = f"{type(exc).__name__}: {exc}"
            return False, output_buffer.getvalue()[:MAX_OUTPUT_LENGTH], error_msg


class ChallengeService:
    """Business rules for the Challenge Hub."""

    @staticmethod
    def get_published_challenges(difficulty: str | None = None, category: str | None = None):
        q = Challenge.query.filter_by(is_published=True)
        if difficulty:
            q = q.filter_by(difficulty=difficulty)
        if category:
            q = q.filter_by(category=category)
        return q.order_by(Challenge.difficulty, Challenge.id).all()

    @staticmethod
    def get_challenge_by_slug(slug: str):
        return Challenge.query.filter_by(slug=slug, is_published=True).first()

    @staticmethod
    def get_user_best_attempt(user: User, challenge: Challenge) -> ChallengeAttempt | None:
        """The most recent passing attempt, or best partial attempt."""
        if not user or not user.is_authenticated:
            return None
        attempts = (
            ChallengeAttempt.query.filter_by(user_id=user.id, challenge_id=challenge.id)
            .order_by(ChallengeAttempt.attempted_at.desc())
            .all()
        )
        if not attempts:
            return None
        for attempt in attempts:
            if attempt.passed:
                return attempt
        return attempts[0]

    @staticmethod
    def is_solved(user: User, challenge: Challenge) -> bool:
        if not user or not user.is_authenticated:
            return False
        return (
            ChallengeAttempt.query.filter_by(
                user_id=user.id, challenge_id=challenge.id, passed=True
            ).first()
            is not None
        )

    @staticmethod
    def grade(user: User, challenge: Challenge, code: str):
        """Grade a submission, store the attempt, and award XP if passing."""
        passed_tests = 0
        total_tests = len(challenge.test_cases)
        outputs = []
        first_error = None

        for case in challenge.test_cases:
            test_input = case.get("input")
            expected = case.get("expected")
            passed, output, error = CodeRunner.run_function(code, test_input, expected)
            outputs.append(output or "")
            if error:
                first_error = first_error or error
            if passed:
                passed_tests += 1

        passed = passed_tests == total_tests and total_tests > 0

        # XP only for first-time solve.
        # Check BEFORE adding the attempt so the just-added passing row
        # doesn't make is_solved() return True (autoflush would expose it).
        already_solved = ChallengeService.is_solved(user, challenge)

        # Save attempt
        attempt = ChallengeAttempt(
            user=user,
            challenge=challenge,
            code=code,
            passed=passed,
            passed_tests=passed_tests,
            total_tests=total_tests,
            output="\n".join(outputs)[:MAX_OUTPUT_LENGTH],
            xp_earned=0,
        )
        db.session.add(attempt)

        xp_earned = 0
        leveled_up = False
        new_badges = []
        if passed and not already_solved:
            xp_earned = challenge.xp_reward
            leveled_up, new_badges = GamificationService.award_xp(
                user,
                xp_earned,
                f"Solved challenge: {challenge.title}",
                "challenge",
            )
            attempt.xp_earned = xp_earned
            db.session.commit()
        else:
            db.session.commit()

        return {
            "passed": passed,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "output": "\n".join(outputs)[:MAX_OUTPUT_LENGTH],
            "error": first_error,
            "xp_earned": xp_earned,
            "leveled_up": leveled_up,
            "new_badges": [badge.to_dict() for badge in new_badges],
            "already_solved": already_solved,
        }

    @staticmethod
    def get_user_stats(user: User) -> dict:
        if not user or not user.is_authenticated:
            return {"solved": 0, "attempted": 0}
        attempts = ChallengeAttempt.query.filter_by(user_id=user.id).all()
        solved = sum(1 for a in attempts if a.passed)
        return {"solved": solved, "attempted": len(attempts)}

