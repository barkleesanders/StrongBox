import pytest
import io
import sys
import contextlib
import importlib
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_dashboard_http_and_refresh_callback(user, monkeypatch):
    from unittest.mock import Mock
    import Camera
    import GUI
    from nicegui import ui

    capture = Mock(return_value="/fixture-frame.jpg")
    monkeypatch.setattr(Camera.Camera, "take_picture", capture)
    launcher = Mock()
    monkeypatch.setattr(ui, "run", launcher)
    monkeypatch.setenv("DISPLAY", "fixture-only")
    monkeypatch.delenv("FORCE_HEADLESS", raising=False)
    GUI.main()
    root = launcher.call_args.kwargs["root"]

    @ui.page("/dashboard")
    def dashboard():
        root()

    await user.open("/dashboard")
    await user.should_see("Strong Box: Air Plant One Mission")
    user.find("PAGE REFRESH").click()
    assert capture.call_count == 4

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
