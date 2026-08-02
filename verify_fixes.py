"""Quick verification of the challenge grading fixes."""
from app.services.challenge_service import CodeRunner

# Multi-argument function: solve(a, b)
code = "def solve(a, b):\n    return a + b\n"
passed, out, err = CodeRunner.run_function(code, [3, 4], 7)
print("multi-arg passed:", passed, "| err:", err)
assert passed and err is None

# Single-argument function: solve(n)
code2 = "def solve(n):\n    return n % 2 == 0\n"
passed2, out2, err2 = CodeRunner.run_function(code2, 4, True)
print("single-arg passed:", passed2, "| err:", err2)
assert passed2 and err2 is None

# Regex import challenge: solve(s)
code3 = (
    "import re\n"
    "def solve(s):\n"
    '    clean = re.sub(r"[^a-zA-Z0-9]", "", s).lower()\n'
    "    return clean == clean[::-1]\n"
)
passed3, out3, err3 = CodeRunner.run_function(code3, "racecar", True)
print("regex passed:", passed3, "| err:", err3)
assert passed3 and err3 is None

# List input (single arg that is a list): solve(nums)
code4 = "def solve(nums):\n    return max(nums)\n"
passed4, out4, err4 = CodeRunner.run_function(code4, [3, 7, 2, 9], 9)
print("list-arg passed:", passed4, "| err:", err4)
assert passed4 and err4 is None

# String arg: solve(s)
code5 = "def solve(s):\n    return s[::-1]\n"
passed5, out5, err5 = CodeRunner.run_function(code5, "hello", "olleh")
print("string-arg passed:", passed5, "| err:", err5)
assert passed5 and err5 is None

print("ALL VERIFICATIONS PASSED ✅")

