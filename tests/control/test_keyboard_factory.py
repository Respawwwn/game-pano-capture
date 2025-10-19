"""Tests for keyboard factory and general functionality."""

import platform

import pytest

from control.keyboard.factory import KeyboardFactory


class TestKeyboardFactoryGeneral:
    """Test general keyboard factory functionality."""

    @pytest.mark.unit
    def test_factory_get_available_platforms(self):
        """Test that factory returns available platforms."""
        platforms = KeyboardFactory.get_available_platforms()
        assert isinstance(platforms, list)
        assert len(platforms) > 0

    @pytest.mark.unit
    def test_factory_get_current_platform(self):
        """Test that factory returns current platform."""
        current = KeyboardFactory.get_current_platform()
        assert isinstance(current, str)
        assert current in ["Darwin", "Windows", "Linux"]

    @pytest.mark.unit
    def test_factory_get_recommended_handler(self):
        """Test that factory returns recommended handler."""
        recommended = KeyboardFactory.get_recommended_handler()
        assert isinstance(recommended, str)
        assert recommended in ["macos", "windows", "generic"]


class TestKeyboardFactoryMacOS:
    """Test keyboard factory functionality on macOS."""

    @pytest.mark.macos
    def test_factory_creates_macos_handler(self):
        """Test that factory creates macOS handler on macOS."""
        KeyboardFactory.clear_cache()
        handler = KeyboardFactory.create_handler()
        assert handler.get_platform_name() == "macOS"

    @pytest.mark.macos
    def test_macos_handler_supports_basic_keys(self):
        """Test that macOS handler supports basic keys."""
        handler = KeyboardFactory.create_handler(force_platform="macos")
        supported_keys = handler.get_supported_keys()

        basic_keys = ["a", "w", "s", "d", "space", "enter"]
        for key in basic_keys:
            assert key in supported_keys, f"macos handler missing key: {key}"


class TestKeyboardFactoryWindows:
    """Test keyboard factory functionality on Windows."""

    @pytest.mark.windows
    def test_factory_creates_windows_handler(self):
        """Test that factory creates Windows handler on Windows."""
        KeyboardFactory.clear_cache()
        handler = KeyboardFactory.create_handler()
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_handler_supports_basic_keys(self):
        """Test that Windows handler supports basic keys."""
        handler = KeyboardFactory.create_handler(force_platform="windows")
        supported_keys = handler.get_supported_keys()

        basic_keys = ["a", "w", "s", "d", "space", "enter"]
        for key in basic_keys:
            assert key in supported_keys, f"windows handler missing key: {key}"


class TestKeyboardFactoryLinux:
    """Test keyboard factory functionality on Linux."""

    @pytest.mark.linux
    def test_factory_creates_generic_handler(self):
        """Test that factory creates generic handler on Linux."""
        KeyboardFactory.clear_cache()
        handler = KeyboardFactory.create_handler()
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_handler_supports_basic_keys(self):
        """Test that generic handler supports basic keys."""
        handler = KeyboardFactory.create_handler(force_platform="generic")
        supported_keys = handler.get_supported_keys()

        basic_keys = ["a", "w", "s", "d", "space", "enter"]
        for key in basic_keys:
            assert key in supported_keys, f"generic handler missing key: {key}"


class TestKeyboardIntegration:
    """Integration tests that require actual system interaction."""

    @pytest.mark.skipif(
        platform.system() not in ["Darwin", "Windows", "Linux"],
        reason="Integration tests require supported platform",
    )
    def test_current_platform_handler_available(self):
        """Test that handler for current platform is available."""
        handler = KeyboardFactory.create_handler()
        assert handler.is_available() in [True, False]  # Should not crash

    @pytest.mark.unit
    def test_key_combination_parsing(self):
        """Test that key combinations are parsed correctly."""
        handler = KeyboardFactory.create_handler()

        # This should not crash (even if it returns False due to no actual key press)
        result = handler.press_key_combination("ctrl+c")
        assert isinstance(result, bool)
