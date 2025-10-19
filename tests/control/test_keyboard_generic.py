"""Tests for generic keyboard handler."""

from unittest.mock import patch

import pytest

from control.keyboard.factory import KeyboardFactory


class TestKeyboardGeneric:
    """Tests for generic keyboard handler."""

    @pytest.mark.linux
    def test_generic_handler_initialization(self):
        """Test generic handler initializes correctly."""
        handler = KeyboardFactory.create_handler(force_platform="generic")
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_press_key_mock_keyboard_lib(self):
        """Test generic key press with mocked keyboard library."""
        handler = KeyboardFactory.create_handler(force_platform="generic")

        # Mock keyboard library
        with patch("keyboard.press") as mock_press, patch(
            "keyboard.release"
        ) as mock_release:
            result = handler.press_key("a", 0.1)

            # Should call keyboard library functions
            mock_press.assert_called_once_with("a")
            mock_release.assert_called_once_with("a")
            assert result is True
