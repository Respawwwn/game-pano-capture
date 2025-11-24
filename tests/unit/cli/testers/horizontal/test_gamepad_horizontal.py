"""Tests for --test-horizontal CLI command with gamepad control."""

import json
from unittest.mock import patch

import pytest


class TestGamepadHorizontalCommand:
    """Test --test-horizontal command with gamepad control."""

    @pytest.fixture
    def gamepad_test_config_file(self, tmp_path):
        """Create a temporary config file with gamepad control game."""
        config_data = {
            "games": {
                "gamepadgame": {
                    "description": "Test game configuration with gamepad control",
                    "control_type": "gamepad",
                    "movement": {
                        "horizontal_steps": 5,
                        "vertical_steps": 3,
                        "pause_between_moves": 0.15,
                    },
                    "screenshot": {"key": "f11", "delay": 0.3, "pause": 0.2},
                    "controls": {
                        "gamepad": {
                            "stick_movement_amount": 0.8,
                            "horizontal_movement_duration": 0.3,
                            "vertical_movement_duration": 0.25,
                        }
                    },
                }
            }
        }

        config_file = tmp_path / "gamepad_test_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        return config_file

    @pytest.mark.unit
    def test_test_horizontal_command_with_gamepad_config(
        self, gamepad_test_config_file, mock_factories, capsys
    ):
        """Test --test-horizontal command with gamepad configuration showing expected output."""
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(gamepad_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("gamepadgame", "horizontal")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Check that it shows the configuration details
        assert "Testing Horizontal Rotation for 'gamepadgame'" in output
        assert "Horizontal steps configured: 5" in output
        assert "Horizontal movement duration: 0.3s" in output
        assert "Pause between moves: 0.15s" in output

        # Check that it explains the test purpose
        assert "360° horizontal rotation" in output
        assert "Focus the game window now!" in output

        # Check that it shows step progression
        assert "Step 1/5" in output
        assert "Step 5/5" in output

        # Check completion message and guidance
        assert "Horizontal Test Complete" in output
        assert "DECREASE 'movement.horizontal_steps'" in output
        assert "INCREASE 'movement.horizontal_steps'" in output

    @pytest.mark.unit
    def test_test_horizontal_command_gamepad_movement_calls(
        self, gamepad_test_config_file, mock_factories, capsys
    ):
        """Test that horizontal movement calls the gamepad handler the correct number of times."""
        from pano_capture import GamePanoCapture

        # Mock time.sleep to speed up tests
        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(gamepad_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method directly
            capturer.test_movement("gamepadgame", "horizontal")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed successfully
        assert "Horizontal Test Complete" in output

        # Get the gamepad handler mock to verify calls
        gamepad_handler = mock_factories["gamepad"].create_handler.return_value

        # For horizontal test with 5 steps: should call move_stick 5 times
        # Based on the gamepad config: stick_movement_amount: 0.8 and horizontal_steps: 5
        assert gamepad_handler.move_stick.call_count == 5

        # Verify all calls were with the correct horizontal movement
        # Based on the gamepad config: stick_movement_amount: 0.8
        expected_calls = [
            ("right", 0.8, 0.0, 0.3)
            for _ in range(5)  # 5 calls with (direction, x, y, duration)
        ]

        actual_calls = [call.args for call in gamepad_handler.move_stick.call_args_list]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_horizontal_command_missing_gamepad_sensitivity(
        self, tmp_path, mock_factories, capsys
    ):
        """Test horizontal movement when gamepad sensitivity is missing - should use default."""
        # Create config without gamepad stick_movement_amount
        config_data = {
            "games": {
                "gamepadgame": {
                    "description": "Test game with missing gamepad sensitivity",
                    "control_type": "gamepad",
                    "movement": {
                        "horizontal_steps": 3,
                        "pause_between_moves": 0.15,
                    },
                    "screenshot": {"key": "f11", "delay": 0.3, "pause": 0.2},
                    "controls": {
                        "gamepad": {
                            "horizontal_movement_duration": 0.3
                            # Note: "stick_movement_amount" is intentionally missing
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

            capturer.test_movement("gamepadgame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Verify the test completed
        assert "Horizontal Test Complete" in output

        # Get the gamepad handler mock
        gamepad_handler = mock_factories["gamepad"].create_handler.return_value

        # Should call move_stick 3 times with default horizontal sensitivity
        assert gamepad_handler.move_stick.call_count == 3

        # Verify all calls used default sensitivity (should be reasonable default like 0.5 or 1.0)
        actual_calls = [call.args for call in gamepad_handler.move_stick.call_args_list]

        # Check that all calls have the correct format (direction, x, y, duration)
        # and horizontal movement pattern
        assert len(actual_calls) == 3
        for call in actual_calls:
            assert len(call) == 4  # (direction, x, y, duration) tuple
            assert call[0] == "right"  # direction should be 'right' for horizontal
            assert call[2] == 0.0  # y should be 0.0 for horizontal movement
            assert call[1] > 0  # x should be positive (rightward movement)
            assert call[3] == 0.3  # duration should match config

    @pytest.mark.unit
    def test_test_horizontal_command_gamepad_failure(
        self, gamepad_test_config_file, mock_factories, capsys
    ):
        """Test horizontal movement when gamepad handler move_stick returns False."""
        from pano_capture import GamePanoCapture

        # Configure gamepad handler to fail on move_stick
        gamepad_handler = mock_factories["gamepad"].create_handler.return_value
        gamepad_handler.move_stick.return_value = False  # Simulate failure

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(gamepad_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("gamepadgame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Should still show test started and completed messages
        assert "Testing Horizontal Rotation for 'gamepadgame'" in output
        assert "Horizontal Test Complete" in output

        # Should attempt all 5 steps even if gamepad fails
        assert gamepad_handler.move_stick.call_count == 5

        # Verify all calls were attempted with correct parameters
        expected_calls = [("right", 0.8, 0.0, 0.3) for _ in range(5)]

        actual_calls = [call.args for call in gamepad_handler.move_stick.call_args_list]
        assert actual_calls == expected_calls

    @pytest.mark.unit
    def test_test_horizontal_command_gamepad_not_available(
        self, gamepad_test_config_file, mock_factories, capsys
    ):
        """Test horizontal movement when gamepad handler is not available."""
        from pano_capture import GamePanoCapture

        # Configure gamepad handler to be unavailable
        gamepad_handler = mock_factories["gamepad"].create_handler.return_value
        gamepad_handler.is_available.return_value = False

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                config_file=str(gamepad_test_config_file),
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            capturer.test_movement("gamepadgame", "horizontal")

        captured = capsys.readouterr()
        output = captured.out

        # Should handle unavailable gamepad gracefully
        assert "Testing Horizontal Rotation for 'gamepadgame'" in output
        # Test should still attempt to complete
        assert "Horizontal Test Complete" in output or "not available" in output.lower()
