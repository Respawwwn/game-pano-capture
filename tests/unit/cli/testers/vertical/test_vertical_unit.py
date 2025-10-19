"""Generic tests for --test-vertical CLI command."""

from unittest.mock import patch

import pytest


class TestVerticalCommand:
    """Generic tests for --test-vertical command."""

    @pytest.mark.unit
    def test_test_vertical_command_with_nonexistent_game(self, mock_factories, capsys):
        """Test --test-vertical command with a non-existent game."""
        from pano_capture import GamePanoCapture

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method with non-existent game
            capturer.test_movement("NonExistentGame123", "vertical")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should display error message
        assert "Game 'NonExistentGame123' not found in config" in output

    @pytest.mark.unit
    def test_test_vertical_command_with_special_characters(
        self, mock_factories, capsys
    ):
        """Test --test-vertical command with special characters in game name."""
        from pano_capture import GamePanoCapture

        game_name = "Test Game: Special Edition (2024)"

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
