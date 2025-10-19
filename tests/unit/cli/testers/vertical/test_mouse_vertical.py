"""Tests for --test-vertical CLI command with mouse control."""

import json
from unittest.mock import patch

import pytest


class TestMouseVerticalCommand:
    """Test --test-vertical command with mouse control."""

    @pytest.fixture
    def mouse_test_config_file(self, tmp_path):
        """Create a temporary config file with mouse control game."""
        config_data = {
            "games": {
                "mousegame": {
                    "description": "Test game configuration with mouse control",
                    "control_type": "mouse",
                    "movement": {
                        "horizontal_steps": 6,
                        "vertical_steps": 4,
                        "horizontal_movement_duration": 0.2,
                        "vertical_movement_duration": 0.25,
                        "pause_between_moves": 0.1,
                    },
                    "screenshot": {"key": "f12", "delay": 0.2, "pause": 0.15},
                    "controls": {"mouse": {"sensitivity": 40}},
                }
            }
        }

        config_file = tmp_path / "mouse_test_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        return config_file

    @pytest.mark.unit
    def test_test_vertical_command_with_mouse_config(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test --test-vertical command with mouse configuration showing expected output."""
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(mouse_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("mousegame", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Check that it shows the configuration details
        assert "Testing Vertical Movement for 'mousegame'" in output
        assert "Vertical steps configured: 4" in output
        assert "Vertical movement duration: 0.25s" in output
        assert "Pause between moves: 0.1s" in output

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
    def test_test_vertical_command_mouse_movement_calls(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test that vertical movement calls the mouse handler the correct number of times."""
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(mouse_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("mousegame", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed successfully
        assert "Vertical Test Complete" in output

        # Get the mouse handler mock to verify calls
        mouse_handler = mock_factories["mouse"].create_handler.return_value

        # For vertical test with 4 steps: should call move_relative 4 times
        # Based on the mouse config: sensitivity: 40 and vertical_steps: 4
        assert mouse_handler.move_relative.call_count == 4

        # Verify all calls were with the correct vertical movement (0 horizontal, 40 pixels down)
        # Based on the mouse config: sensitivity: 40
        expected_calls = [
            (0, 40)
            for _ in range(4)  # 4 calls with (0, 40) movement
        ]

        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_vertical_command_missing_mouse_sensitivity(
        self, tmp_path, mock_factories, capsys
    ):
        """Test vertical movement when mouse sensitivity is missing - should use default."""
        # Create config without mouse sensitivity
        config_data = {
            "games": {
                "mousegame": {
                    "description": "Test game with missing mouse sensitivity",
                    "control_type": "mouse",
                    "movement": {
                        "horizontal_steps": 6,
                        "vertical_steps": 3,
                        "horizontal_movement_duration": 0.2,
                        "vertical_movement_duration": 0.25,
                        "pause_between_moves": 0.1,
                    },
                    "screenshot": {"key": "f12", "delay": 0.2, "pause": 0.15},
                    "controls": {
                        "mouse": {
                            # Note: "sensitivity" is intentionally missing
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "missing_sensitivity_config.json"
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

            capturer.test_movement("mousegame", "vertical")

        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed
        assert "Vertical Test Complete" in output

        # Get the mouse handler mock
        mouse_handler = mock_factories["mouse"].create_handler.return_value

        # Should call move_relative 3 times with default sensitivity
        assert mouse_handler.move_relative.call_count == 3

        # Verify all calls used default sensitivity (should be reasonable default)
        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]

        # Check that all calls have the same vertical movement (whatever the default is)
        # and 0 horizontal movement
        assert len(actual_calls) == 3
        for call in actual_calls:
            assert len(call) == 2  # (x, y) tuple
            assert call[0] == 0  # x should be 0 for vertical movement
            assert call[1] > 0  # y should be positive (downward movement)

    @pytest.mark.unit
    def test_test_vertical_command_mouse_failure(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test vertical movement when mouse handler move_relative returns False."""
        from pano_capture import GamePanoCapture

        # Configure mouse handler to fail on move_relative
        mouse_handler = mock_factories["mouse"].create_handler.return_value
        mouse_handler.move_relative.return_value = False  # Simulate failure

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(mouse_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("mousegame", "vertical")

        captured = capsys.readouterr()
        output = captured.out

        # Should still show test started and completed messages
        assert "Testing Vertical Movement for 'mousegame'" in output
        assert "Vertical Test Complete" in output

        # Should attempt all 4 steps even if mouse fails
        assert mouse_handler.move_relative.call_count == 4

        # Verify all calls were attempted with correct parameters
        expected_calls = [(0, 40) for _ in range(4)]

        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_vertical_command_mouse_not_available(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test vertical movement when mouse handler is not available."""
        from pano_capture import GamePanoCapture

        # Configure mouse handler to be unavailable
        mouse_handler = mock_factories["mouse"].create_handler.return_value
        mouse_handler.is_available.return_value = False

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(mouse_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("mousegame", "vertical")

        captured = capsys.readouterr()
        output = captured.out

        # Should handle unavailable mouse gracefully
        assert "Testing Vertical Movement for 'mousegame'" in output
        # Test should still attempt to complete
        assert "Vertical Test Complete" in output or "not available" in output.lower()

    @pytest.mark.unit
    def test_test_vertical_command_with_special_characters(
        self, mock_factories, capsys
    ):
        """Test --test-vertical command with special characters in game name."""
        from pano_capture import GamePanoCapture

        game_name = "Test Mouse Game: Special Edition (2024)"

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method with special characters
            capturer.test_movement(game_name, "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should handle special characters without crashing
        assert f"Game '{game_name}' not found in config" in output

    @pytest.mark.unit
    def test_test_vertical_command_with_empty_string(self, mock_factories, capsys):
        """Test --test-vertical command with empty game name."""
        from pano_capture import GamePanoCapture

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method with empty string
            capturer.test_movement("", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should handle empty string gracefully
        assert "Game '' not found in config" in output
