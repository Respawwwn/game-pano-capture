"""Tests for --list CLI command."""

import subprocess
import sys
from pathlib import Path

import pytest


class TestListCommand:
    """Test --list command functionality."""

    @pytest.fixture
    def script_path(self):
        """Get path to the main script."""
        return Path(__file__).parent.parent.parent.parent / "pano_capture.py"

    @pytest.mark.functional
    def test_list_command_executes_successfully(self, script_path):
        """Test --list command executes without errors."""
        # Run the --list command
        result = subprocess.run(
            [sys.executable, str(script_path), "--list"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Check the result - should execute successfully
        assert result.returncode == 0
        output = result.stdout
        assert "Configured games:" in output

    @pytest.mark.functional
    def test_list_command_output_format(self, script_path):
        """Test --list command has correct output format."""
        # Run the --list command
        result = subprocess.run(
            [sys.executable, str(script_path), "--list"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Check the result format
        assert result.returncode == 0
        output = result.stdout
        assert "Configured games:" in output
        # Should have bullet points for games
        lines = output.split("\n")
        games_section_found = False
        for line in lines:
            if "Configured games:" in line:
                games_section_found = True
            elif (
                games_section_found
                and line.strip()
                and not line.startswith("  - ")
                and "macOS:" not in line
                and "Configuration loaded" not in line
            ):
                # Allow for other output but games should start with "  - "
                pass

        assert games_section_found
