"""Integration tests for CLI commands - tests that commands run without crashing."""

import subprocess
import sys
from pathlib import Path

import pytest


class TestCLIIntegration:
    """Test CLI integration - commands should execute without errors."""

    @pytest.fixture
    def script_path(self):
        """Get path to the main script."""
        return Path(__file__).parent.parent.parent.parent / "pano_capture.py"

    @pytest.mark.functional
    def test_invalid_argument_shows_error(self, script_path):
        """Test invalid arguments show error."""
        result = subprocess.run(
            [sys.executable, str(script_path), "--invalid-arg"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode != 0
        assert "unrecognized arguments" in result.stderr.lower()

    @pytest.mark.functional
    def test_no_arguments_shows_help(self, script_path):
        """Test running without arguments shows help."""
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert "360° Game Screenshot Automation" in result.stdout
