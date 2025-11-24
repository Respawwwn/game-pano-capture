"""Tests for --test-horizontal CLI command with mouse control."""

import json
from unittest.mock import patch

import pytest


class TestMouseHorizontalCommand:
    """Test --test-horizontal command with mouse control."""

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
                        "vertical_steps": 3,
                        "pause_between_moves": 0.1,
                    },
                    "screenshot": {"key": "f12", "delay": 0.2, "pause": 0.15},
                    "controls": {
                        "mouse": {
                            "horizontal_sensitivity": 50,
                            "vertical_sensitivity": 75,
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "mouse_test_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        return config_file

    @pytest.mark.unit
    def test_test_horizontal_command_with_mouse_config(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test --test-horizontal command with mouse configuration showing expected output."""
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
            capturer.test_movement("mousegame", "horizontal")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Check that it shows the configuration details
        assert "Testing Horizontal Rotation for 'mousegame'" in output
        assert "Horizontal steps configured: 6" in output
        # Mouse controls don't show movement duration (instantaneous movements)
        assert "Horizontal movement duration:" not in output
        assert "Pause between moves: 0.1s" in output

        # Check that it explains the test purpose
        assert "360° horizontal rotation" in output
        assert "Focus the game window now!" in output

        # Check that it shows step progression
        assert "Step 1/6" in output
        assert "Step 6/6" in output

        # Check completion message and guidance
        assert "Horizontal Test Complete" in output
        assert "DECREASE 'movement.horizontal_steps'" in output
        assert "INCREASE 'movement.horizontal_steps'" in output

    @pytest.mark.unit
    def test_test_horizontal_command_mouse_movement_calls(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test that horizontal movement calls the mouse handler the correct number of times."""
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
            capturer.test_movement("mousegame", "horizontal")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed successfully
        assert "Horizontal Test Complete" in output

        # Get the mouse handler mock to verify calls
        mouse_handler = mock_factories["mouse"].create_handler.return_value

        # For horizontal test with 6 steps: should call move_relative 6 times
        # Based on the mouse config: horizontal_sensitivity: 50 and horizontal_steps: 6
        assert mouse_handler.move_relative.call_count == 6

        # Verify all calls were with the correct horizontal movement (50 pixels right, 0 vertical)
        # Based on the mouse config: sensitivity: 50
        expected_calls = [
            (50, 0)
            for _ in range(6)  # 6 calls with (50, 0) movement
        ]

        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_horizontal_command_missing_mouse_sensitivity(
        self, tmp_path, mock_factories, capsys
    ):
        """Test horizontal movement when mouse sensitivity is missing - should use default."""
        # Create config without mouse horizontal_sensitivity
        config_data = {
            "games": {
                "mousegame": {
                    "description": "Test game with missing mouse sensitivity",
                    "control_type": "mouse",
                    "movement": {
                        "horizontal_steps": 4,
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

            capturer.test_movement("mousegame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed
        assert "Horizontal Test Complete" in output

        # Get the mouse handler mock
        mouse_handler = mock_factories["mouse"].create_handler.return_value

        # Should call move_relative 4 times with default horizontal sensitivity
        assert mouse_handler.move_relative.call_count == 4

        # Verify all calls used default sensitivity (should be reasonable default like 10 or 20)
        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]

        # Check that all calls have the same horizontal movement (whatever the default is)
        # and 0 vertical movement
        assert len(actual_calls) == 4
        for call in actual_calls:
            assert len(call) == 2  # (x, y) tuple
            assert call[1] == 0  # y should be 0 for horizontal movement
            assert call[0] > 0  # x should be positive (rightward movement)

    @pytest.mark.unit
    def test_test_horizontal_command_mouse_failure(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test horizontal movement when mouse handler move_relative returns False."""
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

            capturer.test_movement("mousegame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Should still show test started and completed messages
        assert "Testing Horizontal Rotation for 'mousegame'" in output
        assert "Horizontal Test Complete" in output

        # Should attempt all 6 steps even if mouse fails
        assert mouse_handler.move_relative.call_count == 6

        # Verify all calls were attempted with correct parameters
        expected_calls = [(50, 0) for _ in range(6)]

        actual_calls = [
            call.args for call in mouse_handler.move_relative.call_args_list
        ]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_horizontal_command_mouse_not_available(
        self, mouse_test_config_file, mock_factories, capsys
    ):
        """Test horizontal movement when mouse handler is not available."""
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

            capturer.test_movement("mousegame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Should handle unavailable mouse gracefully
        assert "Testing Horizontal Rotation for 'mousegame'" in output
        # Test should still attempt to complete
        assert "Horizontal Test Complete" in output or "not available" in output.lower()
