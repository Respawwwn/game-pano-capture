"""Tests for --test-vertical CLI command with keyboard control."""

import json
from unittest.mock import patch

import pytest


class TestKeyboardVerticalCommand:
    """Test --test-vertical command with keyboard control."""

    @pytest.fixture
    def test_config_file(self, tmp_path):
        """Create a temporary config file with keyboard test game."""
        config_data = {
            "games": {
                "keyboardgame": {
                    "description": "Test game configuration",
                    "control_type": "keyboard",
                    "movement": {
                        "horizontal_steps": 8,
                        "vertical_steps": 4,
                        "pause_between_moves": 0.05,
                    },
                    "screenshot": {"key": "f9", "delay": 0.1, "pause": 0.1},
                    "controls": {
                        "keyboard": {
                            "left": "a",
                            "right": "d",
                            "up": "w",
                            "down": "s",
                            "horizontal_movement_duration": 0.1,
                            "vertical_movement_duration": 0.2,
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "test_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        return config_file

    @pytest.mark.unit
    def test_test_vertical_command_with_test_config(
        self, test_config_file, mock_factories, capsys
    ):
        """Test --test-vertical command with test configuration showing expected output."""
        # Import and create GamePanoCapture with mocked factories
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("keyboardgame", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Check that it shows the configuration details
        assert "Testing Vertical Movement for 'keyboardgame'" in output
        assert "Vertical steps configured: 4" in output
        assert "Vertical movement duration: 0.2s" in output
        assert "Pause between moves: 0.05s" in output

        # Check that it explains the test purpose
        assert "zenith (straight up) to nadir (straight down)" in output
        assert "position camera at ZENITH (straight up)!" in output

        # Check that it shows step progression
        assert "Step 1/4" in output
        assert "Step 4/4" in output

        # Check completion message and guidance
        assert "Vertical Test Complete" in output
        assert "DECREASE 'movement.vertical_steps'" in output
        assert "INCREASE 'movement.vertical_steps'" in output

    @pytest.mark.unit
    def test_test_vertical_command_movement_calls(
        self, test_config_file, mock_factories, capsys
    ):
        """Test that vertical movement calls the keyboard handler the correct number of times."""
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("keyboardgame", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed successfully
        assert "Vertical Test Complete" in output

        # Get the keyboard handler mock to verify calls
        keyboard_handler = mock_factories["keyboard"].create_handler.return_value

        # For vertical test with 4 steps: should call press_key 4 times with "s" (down key)
        # Based on the test config: "down": "s" and vertical_steps: 4
        assert keyboard_handler.press_key.call_count == 4

        # Verify all calls were with the down key ("s") and correct duration (0.2s)
        expected_calls = [
            ("s", 0.2)
            for _ in range(4)  # 4 calls with key "s" and duration 0.2
        ]

        actual_calls = [call.args for call in keyboard_handler.press_key.call_args_list]
        assert actual_calls == expected_calls

        # Verify no screenshot key combinations were called during movement test
        assert keyboard_handler.press_key_combination.call_count == 0

    @pytest.mark.unit
    def test_test_vertical_command_missing_key_mapping(
        self, tmp_path, mock_factories, capsys
    ):
        """Test vertical movement when 'down' key mapping is missing - should fallback to 'down'."""
        # Create config without 'down' key mapping
        config_data = {
            "games": {
                "keyboardgame": {
                    "description": "Test game with missing down key mapping",
                    "control_type": "keyboard",
                    "movement": {
                        "horizontal_steps": 8,
                        "vertical_steps": 3,
                        "pause_between_moves": 0.05,
                    },
                    "screenshot": {"key": "f9", "delay": 0.1, "pause": 0.1},
                    "controls": {
                        "keyboard": {
                            "left": "a",
                            "right": "d",
                            "up": "w",
                            "horizontal_movement_duration": 0.1,
                            "vertical_movement_duration": 0.2,
                            # Note: "down" is intentionally missing
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "missing_key_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        from pano_capture import GamePanoCapture

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("keyboardgame", "vertical")

        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed
        assert "Vertical Test Complete" in output

        # Get the keyboard handler mock
        keyboard_handler = mock_factories["keyboard"].create_handler.return_value

        # Should call press_key 3 times with fallback "down" key (not mapped "s")
        assert keyboard_handler.press_key.call_count == 3

        # Verify all calls used fallback key "down" instead of mapped key
        expected_calls = [
            ("down", 0.2)
            for _ in range(3)  # Should fallback to "down"
        ]

        actual_calls = [call.args for call in keyboard_handler.press_key.call_args_list]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_vertical_command_keyboard_failure(
        self, test_config_file, mock_factories, capsys
    ):
        """Test vertical movement when keyboard handler press_key returns False."""
        from pano_capture import GamePanoCapture

        # Configure keyboard handler to fail on press_key
        keyboard_handler = mock_factories["keyboard"].create_handler.return_value
        keyboard_handler.press_key.return_value = False  # Simulate failure

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("keyboardgame", "vertical")

        captured = capsys.readouterr()
        output = captured.out

        # Should still show test started and completed messages
        assert "Testing Vertical Movement for 'keyboardgame'" in output
        assert "Vertical Test Complete" in output

        # Should attempt all 4 steps even if keyboard fails
        assert keyboard_handler.press_key.call_count == 4

        # Verify all calls were attempted with correct parameters
        expected_calls = [("s", 0.2) for _ in range(4)]

        actual_calls = [call.args for call in keyboard_handler.press_key.call_args_list]
        assert actual_calls == expected_calls
