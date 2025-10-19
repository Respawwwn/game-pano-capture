"""Tests for generic mouse handler."""

from unittest.mock import patch

import pytest

from control.mouse.factory import MouseFactory


class TestMouseGeneric:
    """Tests for generic mouse handler."""

    @pytest.mark.linux
    def test_generic_handler_initialization(self):
        """Test generic handler initializes correctly."""
        handler = MouseFactory.create_handler(force_platform="generic")
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_move_relative_mock_pygame(self):
        """Test generic relative movement with mocked pygame."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components
        with patch("pygame.mouse.set_pos") as mock_set_pos, patch(
            "pygame.mouse.get_pos"
        ) as mock_get_pos:
            mock_get_pos.return_value = (100, 100)

            result = handler.move_relative(10, 20)

            # Should call pygame functions
            mock_get_pos.assert_called_once()
            mock_set_pos.assert_called_once_with((110, 120))
            assert isinstance(result, bool)

    @pytest.mark.linux
    def test_generic_move_absolute_mock_pygame(self):
        """Test generic absolute movement with mocked pygame."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components
        with patch("pygame.mouse.set_pos") as mock_set_pos:
            result = handler.move_absolute(100, 200)

            # Should call pygame functions
            mock_set_pos.assert_called_once_with((100, 200))
            assert isinstance(result, bool)

    @pytest.mark.linux
    def test_generic_get_position_mock_pygame(self):
        """Test generic get position with mocked pygame."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components
        with patch("pygame.mouse.get_pos") as mock_get_pos:
            mock_get_pos.return_value = (150, 250)

            position = handler.get_position()

            # Should call pygame function to get position
            mock_get_pos.assert_called_once()
            assert position == (150, 250)
            assert isinstance(position, tuple)
            assert len(position) == 2

    @pytest.mark.linux
    def test_generic_click_mock_pygame(self):
        """Test generic mouse click with mocked pygame."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components
        with patch("pygame.event.post") as mock_post:
            result = handler.click("left")

            # Should post pygame events for mouse down/up
            assert mock_post.call_count >= 2  # down + up events
            assert isinstance(result, bool)

    @pytest.mark.linux
    def test_generic_scroll_mock_pygame(self):
        """Test generic mouse scroll with mocked pygame."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components
        with patch("pygame.event.post") as mock_post:
            result = handler.scroll(0, 3)

            # Should post pygame scroll events
            mock_post.assert_called()
            assert isinstance(result, bool)

    @pytest.mark.linux
    def test_generic_supported_buttons(self):
        """Test that generic handler supports standard mouse buttons."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Mock pygame components for these tests
        with patch("pygame.event.post"):
            # Test different button types
            for button in ["left", "right", "middle"]:
                result = handler.click(button)
                assert isinstance(result, bool)

    @pytest.mark.linux
    def test_generic_availability_check(self):
        """Test generic handler availability check."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Should return boolean indicating if pygame is available
        availability = handler.is_available()
        assert isinstance(availability, bool)
