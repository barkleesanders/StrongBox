import pytest
import io
import sys
import contextlib
import importlib
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Sample test skeleton for GUI.py

def test_gui_launch():
    # TODO: Replace with actual test
    assert True

import subprocess
import sys
import os

def test_gui_headless_launch():
    """Test that GUI.py handles headless environment gracefully using a subprocess for true isolation."""
    env = os.environ.copy()
    env.pop("DISPLAY", None)  # Remove DISPLAY to simulate headless
    env["FORCE_HEADLESS"] = "1"
    result = subprocess.run([
        sys.executable, os.path.join(os.path.dirname(__file__), "..", "launch_gui.py")
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}"
    assert "No display found" in result.stdout + result.stderr, "Expected error message for headless environment."
