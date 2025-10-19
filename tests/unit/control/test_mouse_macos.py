"""Tests specific to macOS mouse handler."""

from unittest.mock import Mock, patch

import pytest

from control.mouse.factory import MouseFactory


class TestMouseMacOS:
    """Tests specific to macOS mouse handler."""

    @pytest.mark.macos
    def test_macos_handler_initialization(self):
        """Test macOS handler initializes correctly."""
        handler = MouseFactory.create_handler(force_platform="macos")
        assert handler.get_platform_name() == "macOS"
        assert isinstance(handler.is_available(), bool)

    @pytest.mark.macos
    def test_macos_move_relative_mock_quartz(self):
        """Test macOS relative movement with mocked Quartz."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Mock Quartz functions
        with patch("control.mouse.macos.CGEventCreateMouseEvent") as mock_create, patch(
            "control.mouse.macos.CGEventPost"
        ) as mock_post, patch.object(handler, "get_position", return_value=(100, 100)):
            mock_create.return_value = Mock()

            result = handler.move_relative(10, 20)

            # Should call Quartz functions for mouse move
            mock_create.assert_called_once()
            mock_post.assert_called_once()
            assert isinstance(result, bool)

    @pytest.mark.macos
    def test_macos_move_absolute_mock_quartz(self):
        """Test macOS absolute movement with mocked Quartz."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Mock Quartz functions
        with patch("control.mouse.macos.CGEventCreateMouseEvent") as mock_create, patch(
            "control.mouse.macos.CGEventPost"
        ) as mock_post:
            mock_create.return_value = Mock()

            result = handler.move_absolute(100, 200)

            # Should call Quartz functions for mouse move
            mock_create.assert_called_once()
            mock_post.assert_called_once()
            assert isinstance(result, bool)

    @pytest.mark.macos
    def test_macos_click_mock_quartz(self):
        """Test macOS mouse click with mocked Quartz."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Mock Quartz functions
        with patch("control.mouse.macos.CGEventCreateMouseEvent") as mock_create, patch(
            "control.mouse.macos.CGEventPost"
        ) as mock_post, patch.object(handler, "get_position", return_value=(100, 100)):
            mock_create.return_value = Mock()

            result = handler.click("left")

            # Should call Quartz functions for mouse down + up
            assert mock_create.call_count == 2  # down and up events
            assert mock_post.call_count == 2  # post down + post up
            assert isinstance(result, bool)

    @pytest.mark.macos
    def test_macos_scroll_mock_quartz(self):
        """Test macOS mouse scroll with mocked Quartz."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Mock Quartz functions
        with patch(
            "control.mouse.macos.CGEventCreateScrollWheelEvent"
        ) as mock_create, patch("control.mouse.macos.CGEventPost") as mock_post:
            mock_create.return_value = Mock()

            result = handler.scroll(0, 3)

            # Should call Quartz functions for scroll
            mock_create.assert_called_once()
            mock_post.assert_called_once()
            assert isinstance(result, bool)

    @pytest.mark.macos
    def test_macos_get_position_mock_quartz(self):
        """Test macOS get position with mocked Quartz."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Mock Quartz functions
        with patch("control.mouse.macos.CGEventCreateMouseEvent") as mock_create, patch(
            "control.mouse.macos.CGEventGetLocation"
        ) as mock_get_location:
            mock_create.return_value = Mock()
            mock_get_location.return_value = Mock(x=150.0, y=250.0)

            position = handler.get_position()

            # Should call Quartz functions to get position
            mock_create.assert_called_once()
            mock_get_location.assert_called_once()
            assert position == (150, 250)
            assert isinstance(position, tuple)
            assert len(position) == 2
