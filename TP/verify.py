#!/usr/bin/env python
"""Quick test script to verify setup."""

import subprocess
import sys

print("=" * 60)
print("QUICK VERIFICATION")
print("=" * 60)

# Test 1: Lint check
print("\n1. Running lint check...")
result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", "."],
    cwd=".",
    capture_output=True,
    text=True,
    timeout=30
)
if result.returncode == 0:
    print("   ✅ Lint check passed")
else:
    print("   ❌ Lint check failed")
    print(result.stdout)
    print(result.stderr)

# Test 2: Run unit tests only
print("\n2. Running unit tests (without performance)...")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-m", "not performance", "-v"],
    cwd=".",
    capture_output=True,
    text=True,
    timeout=30
)
if result.returncode == 0:
    print("   ✅ Unit tests passed")
else:
    print("   ❌ Unit tests failed")
    print(result.stdout[-500:])  # Last 500 chars

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
