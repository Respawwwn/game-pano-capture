"""Tests specific to Windows keyboard handler."""

from unittest.mock import Mock, patch

import pytest

from control.keyboard.factory import KeyboardFactory


class TestKeyboardWindows:
    """Tests specific to Windows keyboard handler."""

    @pytest.mark.windows
    def test_windows_handler_initialization(self):
        """Test Windows handler initializes correctly."""
        handler = KeyboardFactory.create_handler(force_platform="windows")
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_press_key_mock_win32(self):
        """Test Windows key press with mocked win32api."""
        handler = KeyboardFactory.create_handler(force_platform="windows")

        # Mock win32api
        with patch("control.keyboard.windows.win32api", create=True) as mock_win32:
            mock_win32.keybd_event = Mock()

            result = handler.press_key("a", 0.1)

            # Should call win32 functions
            assert mock_win32.keybd_event.call_count >= 2  # key down + key up
            assert result is True
