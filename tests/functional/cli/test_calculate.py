"""Tests for --calculate CLI command integration."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestCalculateCommandIntegration:
    """Test --calculate command integration."""

    @pytest.fixture
    def script_path(self):
        """Get path to the main script."""
        return Path(__file__).parent.parent.parent.parent / "pano_capture.py"

    @pytest.fixture
    def test_config_file(self, tmp_path):
        """Create a temporary config file with test game."""
        config_data = {
            "games": {
                "foobar": {
                    "description": "Configuration for foobar",
                    "control_type": "keyboard",
                    "movement": {
                        "horizontal_steps": 11,
                        "vertical_steps": 6,
                        "pause_between_moves": 0.2,
                    },
                    "screenshot": {"key": "alt+4", "delay": 0.3, "pause": 0.2},
                    "controls": {
                        "keyboard": {
                            "left": "j",
                            "right": "l",
                            "up": "i",
                            "down": "k",
                            "horizontal_movement_duration": 0.5,
                            "vertical_movement_duration": 0.4,
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "test_game_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        return config_file

    @pytest.mark.functional
    def test_calculate_command_output_details(self, script_path, test_config_file):
        """Test --calculate command output contains expected details."""
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--config",
                str(test_config_file),
                "--calculate",
                "foobar",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        output = result.stdout

        # Check for specific configuration values from foobar config
        assert "Horizontal steps: 11" in output
        assert "Vertical steps: 6" in output
        assert "Control type: keyboard" in output

        # Check for timing information
        assert "Horizontal movement duration: 0.5s" in output
        assert "Vertical movement duration: 0.4s" in output
        assert "Pause between moves: 0.2s" in output
        assert "Screenshot delay: 0.3s" in output
        assert "Screenshot pause: 0.2s" in output

        # Check for calculated statistics
        assert "Total screenshots: 77" in output
        assert "Horizontal movements: 70" in output
        assert "Vertical movements: 6" in output

        # Check for time estimates
        assert "Initial countdown: 5s" in output
        assert "Screenshot time: 38.5s" in output
        assert "Vertical movement time: 3.6s" in output
        assert "Screenshot time: 38.5s" in output
        assert "Total estimated time: 96.1s (1.6 minutes)" in output

        # Check for capture pattern description
        assert "Start position: Zenith (straight up)" in output
        assert "End position: Nadir (straight down)" in output
        assert "Pattern: 7 horizontal rings, 11 shots per ring" in output

        # Based on foobar config: 11 horizontal steps, 6 vertical steps
        # Should result in 77 total screenshots (11 * 7 rings = 77)
        assert "Total screenshots: 77" in output

        # Check movement counts
        assert "Horizontal movements: 70" in output  # (11-1) * 7 = 70
        assert "Vertical movements: 6" in output  # 6 vertical movements

        # Check pattern description matches config
        assert "7 horizontal rings, 11 shots per ring" in output

    @pytest.mark.functional
    def test_calculate_command_with_nonexistent_game(
        self, script_path, test_config_file
    ):
        """Test --calculate command with a non-existent game."""
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--config",
                str(test_config_file),
                "--calculate",
                "NonExistentGame123",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should handle the error gracefully
        assert result.returncode in [0, 1]  # Allow for expected errors
        output = result.stdout + result.stderr
        assert len(output) > 0

    @pytest.mark.functional
    def test_calculate_command_with_special_characters(
        self, script_path, test_config_file
    ):
        """Test --calculate command with special characters in game name."""
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--config",
                str(test_config_file),
                "--calculate",
                "Test Game: Special Edition (2024)",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should handle special characters without crashing
        assert result.returncode in [0, 1]  # Allow for config errors
        output = result.stdout + result.stderr
        assert len(output) > 0

    @pytest.mark.functional
    def test_calculate_command_with_empty_string(self, script_path, test_config_file):
        """Test --calculate command with empty game name."""
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--config",
                str(test_config_file),
                "--calculate",
                "",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should handle empty string gracefully
        assert result.returncode in [0, 1]  # Allow for expected errors
        output = result.stdout + result.stderr
        assert len(output) > 0
