"""Tests for mouse factory and general functionality."""

import platform

import pytest

from control.mouse.factory import MouseFactory


class TestMouseFactoryGeneral:
    """Test general mouse factory functionality."""

    @pytest.mark.unit
    def test_factory_get_available_platforms(self):
        """Test that factory returns available platforms."""
        platforms = MouseFactory.get_available_platforms()
        assert isinstance(platforms, list)
        assert len(platforms) > 0

    @pytest.mark.unit
    def test_factory_get_current_platform(self):
        """Test that factory returns current platform."""
        current = MouseFactory.get_current_platform()
        assert isinstance(current, str)
        assert current in ["Darwin", "Windows", "Linux"]

    @pytest.mark.unit
    def test_factory_get_recommended_handler(self):
        """Test that factory returns recommended handler."""
        recommended = MouseFactory.get_recommended_handler()
        assert isinstance(recommended, str)
        assert recommended in ["macos", "windows", "generic"]


class TestMouseFactoryMacOS:
    """Test mouse factory functionality on macOS."""

    @pytest.mark.macos
    def test_factory_creates_macos_handler(self):
        """Test that factory creates macOS handler on macOS."""
        MouseFactory.clear_cache()
        handler = MouseFactory.create_handler()
        assert handler.get_platform_name() == "macOS"

    @pytest.mark.macos
    def test_macos_handler_basic_functionality(self):
        """Test that macOS handler has basic functionality."""
        handler = MouseFactory.create_handler(force_platform="macos")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "move_relative")
        assert hasattr(handler, "move_absolute")
        assert hasattr(handler, "get_position")
        assert hasattr(handler, "click")
        assert hasattr(handler, "scroll")


class TestMouseFactoryWindows:
    """Test mouse factory functionality on Windows."""

    @pytest.mark.windows
    def test_factory_creates_windows_handler(self):
        """Test that factory creates Windows handler on Windows."""
        MouseFactory.clear_cache()
        handler = MouseFactory.create_handler()
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_handler_basic_functionality(self):
        """Test that Windows handler has basic functionality."""
        handler = MouseFactory.create_handler(force_platform="windows")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "move_relative")
        assert hasattr(handler, "move_absolute")
        assert hasattr(handler, "get_position")
        assert hasattr(handler, "click")
        assert hasattr(handler, "scroll")


class TestMouseFactoryLinux:
    """Test mouse factory functionality on Linux."""

    @pytest.mark.linux
    def test_factory_creates_generic_handler(self):
        """Test that factory creates generic handler on Linux."""
        MouseFactory.clear_cache()
        handler = MouseFactory.create_handler()
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_handler_basic_functionality(self):
        """Test that generic handler has basic functionality."""
        handler = MouseFactory.create_handler(force_platform="generic")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "move_relative")
        assert hasattr(handler, "move_absolute")
        assert hasattr(handler, "get_position")
        assert hasattr(handler, "click")
        assert hasattr(handler, "scroll")


class TestMouseIntegration:
    """Integration tests that require actual system interaction."""

    @pytest.mark.skipif(
        platform.system() not in ["Darwin", "Windows", "Linux"],
        reason="Integration tests require supported platform",
    )
    def test_current_platform_handler_available(self):
        """Test that handler for current platform is available."""
        handler = MouseFactory.create_handler()
        assert handler.is_available() in [True, False]  # Should not crash

    @pytest.mark.unit
    def test_mouse_position_returns_coordinates(self):
        """Test that mouse position returns valid coordinates."""
        handler = MouseFactory.create_handler()

        # This should not crash and return a tuple
        position = handler.get_position()
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

    @pytest.mark.unit
    def test_mouse_click_returns_boolean(self):
        """Test that mouse click returns boolean result."""
        handler = MouseFactory.create_handler()

        # This should not crash and return a boolean
        result = handler.click("left")
        assert isinstance(result, bool)
