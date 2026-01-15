#!/usr/bin/env python3
"""
Simple test runner to verify the auth tests work.
"""

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_auth.py", "-v", "--tb=short"],
        capture_output=False
    )
    sys.exit(result.returncode)
