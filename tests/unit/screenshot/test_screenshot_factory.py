"""Tests for screenshot factory and general functionality."""

from unittest.mock import Mock

import pytest

from screenshot.built_in import BuiltInHandler
from screenshot.external_app import ExternalAppHandler
from screenshot.factory import create_handler
from screenshot.interface import ScreenshotHandler


class TestScreenshotFactoryGeneral:
    """Test general screenshot factory functionality."""

    @pytest.mark.unit
    def test_factory_creates_external_app_handler(self):
        """Test that factory creates external app handler."""
        mock_keyboard = Mock()
        handler = create_handler("external_app", mock_keyboard)

        assert isinstance(handler, ExternalAppHandler)
        assert isinstance(handler, ScreenshotHandler)
        assert handler.keyboard_handler is mock_keyboard

    @pytest.mark.unit
    def test_factory_creates_built_in_handler(self):
        """Test that factory creates built-in handler."""
        handler = create_handler("built_in")

        assert isinstance(handler, BuiltInHandler)
        assert isinstance(handler, ScreenshotHandler)

    @pytest.mark.unit
    def test_factory_external_app_requires_keyboard_handler(self):
        """Test that external_app requires keyboard_handler parameter."""
        with pytest.raises(ValueError, match="keyboard_handler is required"):
            create_handler("external_app", None)

    @pytest.mark.unit
    def test_factory_external_app_without_keyboard_handler(self):
        """Test that external_app without keyboard_handler raises error."""
        with pytest.raises(ValueError, match="keyboard_handler is required"):
            create_handler("external_app")

    @pytest.mark.unit
    def test_factory_built_in_ignores_keyboard_handler(self):
        """Test that built_in handler ignores keyboard_handler parameter."""
        mock_keyboard = Mock()
        handler = create_handler("built_in", mock_keyboard)

        assert isinstance(handler, BuiltInHandler)
        # Built-in handler should not have keyboard_handler attribute
        assert not hasattr(handler, "keyboard_handler")

    @pytest.mark.unit
    def test_factory_unsupported_type_raises_error(self):
        """Test that unsupported screenshot type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported screenshot type: invalid"):
            create_handler("invalid")

    @pytest.mark.unit
    def test_factory_case_sensitive_type(self):
        """Test that screenshot type is case sensitive."""
        mock_keyboard = Mock()

        # These should fail (case sensitivity)
        with pytest.raises(ValueError):
            create_handler("External_App", mock_keyboard)

        with pytest.raises(ValueError):
            create_handler("BUILT_IN")

        with pytest.raises(ValueError):
            create_handler("external_APP", mock_keyboard)

    @pytest.mark.unit
    def test_factory_empty_string_type(self):
        """Test that empty string type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported screenshot type"):
            create_handler("")

    @pytest.mark.unit
    def test_factory_none_type(self):
        """Test that None type raises appropriate error."""
        with pytest.raises((ValueError, TypeError)):
            create_handler(None)


class TestScreenshotHandlerInterface:
    """Test that created handlers implement the interface correctly."""

    @pytest.mark.unit
    def test_external_app_handler_interface(self):
        """Test that external app handler implements required interface."""
        mock_keyboard = Mock()
        handler = create_handler("external_app", mock_keyboard)

        # Should have take_screenshot method
        assert hasattr(handler, "take_screenshot")
        assert callable(handler.take_screenshot)

    @pytest.mark.unit
    def test_built_in_handler_interface(self):
        """Test that built-in handler implements required interface."""
        handler = create_handler("built_in")

        # Should have take_screenshot method
        assert hasattr(handler, "take_screenshot")
        assert callable(handler.take_screenshot)


class TestScreenshotFactoryIntegration:
    """Integration tests for screenshot factory."""

    @pytest.mark.unit
    def test_supported_screenshot_types(self):
        """Test all supported screenshot types can be created."""
        mock_keyboard = Mock()

        # Test external_app
        handler1 = create_handler("external_app", mock_keyboard)
        assert isinstance(handler1, ExternalAppHandler)

        # Test built_in (this might raise ImportError if mss not available)
        try:
            handler2 = create_handler("built_in")
            assert isinstance(handler2, BuiltInHandler)
        except ImportError:
            # mss library not available, which is expected in some test environments
            pytest.skip("mss library not available for built-in screenshots")

    @pytest.mark.unit
    def test_factory_error_messages_helpful(self):
        """Test that factory provides helpful error messages."""
        # Test unsupported type
        with pytest.raises(ValueError) as exc_info:
            create_handler("unsupported_type")

        error_msg = str(exc_info.value)
        assert "unsupported_type" in error_msg
        assert "external_app" in error_msg
        assert "built_in" in error_msg

    @pytest.mark.unit
    def test_factory_with_various_keyboard_handlers(self):
        """Test factory works with different keyboard handler implementations."""
        # Test with different mock configurations
        mock_keyboards = [
            Mock(),
            Mock(spec=["press_key_combination"]),
            Mock(press_key_combination=Mock(return_value=True)),
        ]

        for mock_kb in mock_keyboards:
            handler = create_handler("external_app", mock_kb)
            assert isinstance(handler, ExternalAppHandler)
            assert handler.keyboard_handler is mock_kb
