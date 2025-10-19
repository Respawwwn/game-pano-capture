"""Tests specific to Windows mouse handler."""

from unittest.mock import patch

import pytest

from control.mouse.factory import MouseFactory


class TestMouseWindows:
    """Tests specific to Windows mouse handler."""

    @pytest.mark.windows
    def test_windows_handler_initialization(self):
        """Test Windows handler initializes correctly."""
        handler = MouseFactory.create_handler(force_platform="windows")
        assert handler.get_platform_name() == "Windows"
        assert isinstance(handler.is_available(), bool)

    @pytest.mark.windows
    def test_windows_move_relative_mock_win32(self):
        """Test Windows relative movement with mocked win32api."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32api"
        ) as mock_api:
            result = handler.move_relative(10, 20)

            # Should call win32 functions
            mock_api.SetCursorPos.assert_called()
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_windows_move_absolute_mock_win32(self):
        """Test Windows absolute movement with mocked win32api."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32api"
        ) as mock_api:
            result = handler.move_absolute(100, 200)

            # Should call win32 functions
            mock_api.SetCursorPos.assert_called_with((100, 200))
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_windows_click_mock_win32(self):
        """Test Windows mouse click with mocked win32api."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32api"
        ) as mock_api:
            result = handler.click("left")

            # Should call win32 functions for mouse down/up
            assert mock_api.mouse_event.call_count >= 2  # down + up
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_windows_scroll_mock_win32(self):
        """Test Windows mouse scroll with mocked win32api."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32api"
        ) as mock_api:
            result = handler.scroll(0, 3)

            # Should call win32 functions for scroll
            mock_api.mouse_event.assert_called()
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_windows_get_position_mock_win32(self):
        """Test Windows get position with mocked win32api."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32gui"
        ) as mock_gui:
            mock_gui.GetCursorPos.return_value = (150, 250)

            position = handler.get_position()

            # Should call win32 function to get position
            mock_gui.GetCursorPos.assert_called_once()
            assert position == (150, 250)
            assert isinstance(position, tuple)
            assert len(position) == 2

    @pytest.mark.windows
    def test_windows_supported_buttons(self):
        """Test that Windows handler supports standard mouse buttons."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Mock win32 components for these tests
        with patch.object(handler, "_win32_available", True), patch.object(
            handler, "_win32api"
        ):
            # Test different button types
            for button in ["left", "right", "middle"]:
                result = handler.click(button)
                assert isinstance(result, bool)
