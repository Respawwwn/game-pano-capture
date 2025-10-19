"""Tests specific to macOS keyboard handler."""

from unittest.mock import Mock, patch

import pytest

from control.keyboard.factory import KeyboardFactory


class TestKeyboardMacOS:
    """Tests specific to macOS keyboard handler."""

    @pytest.mark.macos
    def test_macos_handler_initialization(self):
        """Test macOS handler initializes correctly."""
        handler = KeyboardFactory.create_handler(force_platform="macos")
        assert handler.get_platform_name() == "macOS"
        assert isinstance(handler.get_supported_keys(), list)

    @pytest.mark.macos
    def test_macos_key_codes_mapping(self):
        """Test that macOS handler has proper key code mappings."""
        handler = KeyboardFactory.create_handler(force_platform="macos")

        # Test some known macOS key codes
        assert hasattr(handler, "_key_codes")
        assert "a" in handler._key_codes
        assert "space" in handler._key_codes
        assert "enter" in handler._key_codes

    @pytest.mark.macos
    def test_macos_press_key_mock_quartz(self):
        """Test macOS key press with mocked Quartz."""
        handler = KeyboardFactory.create_handler(force_platform="macos")

        # Mock Quartz components
        with patch.object(handler, "_quartz_available", True), patch.object(
            handler, "_cgEvent"
        ) as mock_event, patch.object(handler, "_cgPost") as mock_post:
            mock_event.return_value = Mock()

            result = handler.press_key("a", 0.1)

            # Should call Quartz functions
            assert mock_event.call_count == 2  # key down + key up
            assert mock_post.call_count == 2  # post down + post up
            assert result is True
