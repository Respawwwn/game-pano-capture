"""Tests specific to macOS gamepad handler."""

import pytest

from control.gamepad.factory import GamepadFactory


class TestGamepadMacOS:
    """Tests specific to macOS gamepad handler."""

    @pytest.mark.macos
    def test_macos_handler_initialization(self):
        """Test macOS handler initializes correctly."""
        handler = GamepadFactory.create_handler(force_platform="macos")
        assert handler.get_platform_name() == "macOS"

    @pytest.mark.macos
    def test_macos_handler_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for initialization."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError on initialize
        with pytest.raises(
            NotImplementedError, match="not available for macOS platform"
        ):
            handler.initialize()

    @pytest.mark.macos
    def test_macos_handler_move_stick_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for move_stick."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.move_stick("right", 0.5, 0.0, 0.1)

    @pytest.mark.macos
    def test_macos_handler_press_button_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for press_button."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_button("a", 0.1)

    @pytest.mark.macos
    def test_macos_handler_press_trigger_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for press_trigger."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_trigger("right", 0.5, 0.1)

    @pytest.mark.macos
    def test_macos_handler_press_dpad_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for press_dpad."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_dpad("up", 0.1)

    @pytest.mark.macos
    def test_macos_handler_release_all_not_implemented(self):
        """Test that macOS handler raises NotImplementedError for release_all."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.release_all()

    @pytest.mark.macos
    def test_macos_handler_is_available(self):
        """Test that macOS handler reports as not available."""
        handler = GamepadFactory.create_handler(force_platform="macos")

        # macOS gamepad handler should report as not available
        assert handler.is_available() is False

    @pytest.mark.macos
    def test_macos_handler_platform_name(self):
        """Test that macOS handler returns correct platform name."""
        handler = GamepadFactory.create_handler(force_platform="macos")
        assert handler.get_platform_name() == "macOS"
