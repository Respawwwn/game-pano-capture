"""Tests for gamepad factory and general functionality."""

import platform

import pytest

from control.gamepad.factory import GamepadFactory


class TestGamepadFactoryGeneral:
    """Test general gamepad factory functionality."""

    @pytest.mark.unit
    def test_factory_get_available_platforms(self):
        """Test that factory returns available platforms."""
        platforms = GamepadFactory.get_available_platforms()
        assert isinstance(platforms, list)
        assert len(platforms) > 0

    @pytest.mark.unit
    def test_factory_get_current_platform(self):
        """Test that factory returns current platform."""
        current = GamepadFactory.get_current_platform()
        assert isinstance(current, str)
        assert current in ["Darwin", "Windows", "Linux"]

    @pytest.mark.unit
    def test_factory_get_recommended_handler(self):
        """Test that factory returns recommended handler."""
        recommended = GamepadFactory.get_recommended_handler()
        assert isinstance(recommended, str)
        assert recommended in ["macos", "windows", "generic"]


class TestGamepadFactoryMacOS:
    """Test gamepad factory functionality on macOS."""

    @pytest.mark.macos
    def test_factory_creates_macos_handler(self):
        """Test that factory creates macOS handler on macOS."""
        GamepadFactory.clear_cache()
        handler = GamepadFactory.create_handler()
        assert handler.get_platform_name() == "macOS"

    @pytest.mark.macos
    def test_macos_handler_basic_functionality(self):
        """Test that macOS handler has basic functionality."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "initialize")
        assert hasattr(handler, "move_stick")
        assert hasattr(handler, "press_button")
        assert hasattr(handler, "press_trigger")
        assert hasattr(handler, "press_dpad")
        assert hasattr(handler, "release_all")

    @pytest.mark.macos
    def test_macos_handler_initialization(self):
        """Test that macOS handler initialization raises NotImplementedError."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # Initialize should raise NotImplementedError on macOS
        with pytest.raises(NotImplementedError):
            handler.initialize()


class TestGamepadFactoryWindows:
    """Test gamepad factory functionality on Windows."""

    @pytest.mark.windows
    def test_factory_creates_windows_handler(self):
        """Test that factory creates Windows handler on Windows."""
        GamepadFactory.clear_cache()
        handler = GamepadFactory.create_handler()
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_handler_basic_functionality(self):
        """Test that Windows handler has basic functionality."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "initialize")
        assert hasattr(handler, "move_stick")
        assert hasattr(handler, "press_button")
        assert hasattr(handler, "press_trigger")
        assert hasattr(handler, "press_dpad")
        assert hasattr(handler, "release_all")

    @pytest.mark.windows
    def test_windows_handler_initialization(self):
        """Test that Windows handler initialization works."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Initialize should return boolean
        result = handler.initialize()
        assert isinstance(result, bool)


class TestGamepadFactoryLinux:
    """Test gamepad factory functionality on Linux."""

    @pytest.mark.linux
    def test_factory_creates_generic_handler(self):
        """Test that factory creates generic handler on Linux."""
        GamepadFactory.clear_cache()
        handler = GamepadFactory.create_handler()
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_handler_basic_functionality(self):
        """Test that generic handler has basic functionality."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Test basic methods exist and return appropriate types
        assert hasattr(handler, "initialize")
        assert hasattr(handler, "move_stick")
        assert hasattr(handler, "press_button")
        assert hasattr(handler, "press_trigger")
        assert hasattr(handler, "press_dpad")
        assert hasattr(handler, "release_all")

    @pytest.mark.linux
    def test_generic_handler_initialization(self):
        """Test that generic handler initialization raises NotImplementedError."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Initialize should raise NotImplementedError on Linux
        with pytest.raises(NotImplementedError):
            handler.initialize()


class TestGamepadIntegration:
    """Integration tests that require actual system interaction."""

    @pytest.mark.skipif(
        platform.system() not in ["Darwin", "Windows", "Linux"],
        reason="Integration tests require supported platform",
    )
    def test_current_platform_handler_available(self):
        """Test that handler for current platform is available."""
        handler = GamepadFactory.create_handler()
        assert handler.is_available() in [True, False]  # Should not crash

    @pytest.mark.unit
    def test_move_stick_behavior(self):
        """Test that move_stick behaves correctly for current platform."""
        handler = GamepadFactory.create_handler()

        # On macOS/Linux, should raise NotImplementedError
        # On Windows with vgamepad, should return boolean
        try:
            result = handler.move_stick("right", 0.5, 0.0, 0.1)
            assert isinstance(result, bool)
        except NotImplementedError:
            # Expected on macOS/Linux
            assert platform.system() in ["Darwin", "Linux"]

    @pytest.mark.unit
    def test_press_button_behavior(self):
        """Test that press_button behaves correctly for current platform."""
        handler = GamepadFactory.create_handler()

        # On macOS/Linux, should raise NotImplementedError
        # On Windows with vgamepad, should return boolean
        try:
            result = handler.press_button("a", 0.1)
            assert isinstance(result, bool)
        except NotImplementedError:
            # Expected on macOS/Linux
            assert platform.system() in ["Darwin", "Linux"]

    @pytest.mark.unit
    def test_press_trigger_behavior(self):
        """Test that press_trigger behaves correctly for current platform."""
        handler = GamepadFactory.create_handler()

        # On macOS/Linux, should raise NotImplementedError
        # On Windows with vgamepad, should return boolean
        try:
            result = handler.press_trigger("right", 0.5, 0.1)
            assert isinstance(result, bool)
        except NotImplementedError:
            # Expected on macOS/Linux
            assert platform.system() in ["Darwin", "Linux"]

    @pytest.mark.unit
    def test_press_dpad_behavior(self):
        """Test that press_dpad behaves correctly for current platform."""
        handler = GamepadFactory.create_handler()

        # On macOS/Linux, should raise NotImplementedError
        # On Windows with vgamepad, should return boolean
        try:
            result = handler.press_dpad("up", 0.1)
            assert isinstance(result, bool)
        except NotImplementedError:
            # Expected on macOS/Linux
            assert platform.system() in ["Darwin", "Linux"]

    @pytest.mark.unit
    def test_release_all_behavior(self):
        """Test that release_all behaves correctly for current platform."""
        handler = GamepadFactory.create_handler()

        # On macOS/Linux, should raise NotImplementedError
        # On Windows with vgamepad, should return boolean
        try:
            result = handler.release_all()
            assert isinstance(result, bool)
        except NotImplementedError:
            # Expected on macOS/Linux
            assert platform.system() in ["Darwin", "Linux"]


class TestGamepadFactoryErrorHandling:
    """Test gamepad factory error handling."""

    @pytest.mark.unit
    def test_factory_invalid_platform_raises_error(self):
        """Test that factory raises error for invalid platform."""
        with pytest.raises(RuntimeError, match="Unsupported gamepad handler"):
            GamepadFactory.create_handler(force_platform="invalid")

    @pytest.mark.unit
    def test_factory_cache_behavior(self):
        """Test that factory caches handlers properly."""
        GamepadFactory.clear_cache()

        # First call should create new handler
        handler1 = GamepadFactory.create_handler()

        # Second call should return same handler (cached)
        handler2 = GamepadFactory.create_handler()
        assert handler1 is handler2

        # Forced platform should not use cache
        handler3 = GamepadFactory.create_handler(force_platform="generic")
        assert handler3 is not handler1

    @pytest.mark.unit
    def test_factory_clear_cache(self):
        """Test that factory cache clearing works."""
        GamepadFactory.clear_cache()
        handler1 = GamepadFactory.create_handler()

        # Clear cache and create new handler
        GamepadFactory.clear_cache()
        handler2 = GamepadFactory.create_handler()

        # Should be different instances after cache clear
        assert handler1 is not handler2


class TestGamepadStickMovement:
    """Test gamepad stick movement functionality."""

    @pytest.mark.windows
    def test_stick_movement_parameters(self):
        """Test that stick movement accepts valid parameters on Windows."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Test valid stick names
        valid_sticks = ["left", "right"]
        for stick in valid_sticks:
            result = handler.move_stick(stick, 0.0, 0.0, 0.1)
            assert isinstance(result, bool)

        # Test valid coordinate ranges
        coordinates = [(-1.0, -1.0), (0.0, 0.0), (1.0, 1.0), (0.5, -0.5)]
        for x, y in coordinates:
            result = handler.move_stick("right", x, y, 0.1)
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_button_press_parameters(self):
        """Test that button press accepts valid parameters on Windows."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Test common button names
        common_buttons = ["a", "b", "x", "y", "start", "select"]
        for button in common_buttons:
            result = handler.press_button(button, 0.1)
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_trigger_press_parameters(self):
        """Test that trigger press accepts valid parameters on Windows."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Test trigger names
        triggers = ["left", "right"]
        for trigger in triggers:
            result = handler.press_trigger(trigger, 0.5, 0.1)
            assert isinstance(result, bool)

        # Test trigger value ranges
        values = [0.0, 0.25, 0.5, 0.75, 1.0]
        for value in values:
            result = handler.press_trigger("right", value, 0.1)
            assert isinstance(result, bool)

    @pytest.mark.windows
    def test_dpad_press_parameters(self):
        """Test that dpad press accepts valid parameters on Windows."""
        handler = GamepadFactory.create_handler(force_platform="windows")

        # Test dpad directions
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            result = handler.press_dpad(direction, 0.1)
            assert isinstance(result, bool)
