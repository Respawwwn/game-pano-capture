"""Tests for CLI help and general functionality."""

import subprocess
import sys
from pathlib import Path

import pytest


class TestHelpAndGeneral:
    """Test help command and general CLI functionality."""

    @pytest.fixture
    def script_path(self):
        """Get path to the main script."""
        return Path(__file__).parent.parent.parent.parent / "pano_capture.py"

    @pytest.mark.functional
    def test_help_command(self, script_path):
        """Test --help command displays help information."""
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Check the result
        assert result.returncode == 0
        output = result.stdout
        assert "360° Game Screenshot Automation" in output
        assert "--list" in output
        assert "--capture" in output
        assert "--setup" in output

    @pytest.mark.functional
    def test_help_shows_all_commands(self, script_path):
        """Test that help shows all available commands."""
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = result.stdout
        expected_commands = [
            "--setup",
            "--capture",
            "--test-horizontal",
            "--test-vertical",
            "--test-screenshot",
            "--calculate",
            "--list",
            "--debug",
        ]

        for command in expected_commands:
            assert command in output

    @pytest.mark.functional
    def test_help_command_descriptions(self, script_path):
        """Test that help command shows command descriptions."""
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = result.stdout
        # Check for key description phrases
        assert "Setup configuration for a game" in output
        assert "Capture panorama for specified game" in output
        assert "List configured games" in output
        assert "Enable debug mode" in output
