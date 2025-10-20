"""Generic tests for --test-horizontal CLI command."""

from unittest.mock import patch

import pytest


class TestHorizontalCommand:
    """Generic tests for --test-horizontal command."""

    @pytest.mark.unit
    def test_test_horizontal_command_with_nonexistent_game(
        self, mock_factories, capsys
    ):
        """Test --test-horizontal command with a non-existent game."""
        from pano_capture import GamePanoCapture

        with patch("time.sleep"):
            capturer = GamePanoCapture(
                keyboard_factory=mock_factories["keyboard"],
                mouse_factory=mock_factories["mouse"],
                gamepad_factory=mock_factories["gamepad"],
            )

            # Call the test method with non-existent game
            capturer.test_movement("NonExistentGame123", "horizontal")

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should display error message
        assert "Game 'NonExistentGame123' not found in config" in output
