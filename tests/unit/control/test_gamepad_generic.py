"""Tests specific to generic gamepad handler (Linux)."""

import pytest

from control.gamepad.factory import GamepadFactory


class TestGamepadGeneric:
    """Tests specific to generic gamepad handler (Linux)."""

    @pytest.mark.linux
    def test_generic_handler_initialization(self):
        """Test generic handler initializes correctly."""
        handler = GamepadFactory.create_handler(force_platform="generic")
        assert handler.get_platform_name() == "Linux/Generic"

    @pytest.mark.linux
    def test_generic_handler_not_implemented(self):
        """Test that generic handler raises NotImplementedError for initialization."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError on initialize
        with pytest.raises(
            NotImplementedError, match="not available for Linux platform"
        ):
            handler.initialize()

    @pytest.mark.linux
    def test_generic_handler_move_stick_not_implemented(self):
        """Test that generic handler raises NotImplementedError for move_stick."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.move_stick("right", 0.5, 0.0, 0.1)

    @pytest.mark.linux
    def test_generic_handler_press_button_not_implemented(self):
        """Test that generic handler raises NotImplementedError for press_button."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_button("a", 0.1)

    @pytest.mark.linux
    def test_generic_handler_press_trigger_not_implemented(self):
        """Test that generic handler raises NotImplementedError for press_trigger."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_trigger("right", 0.5, 0.1)

    @pytest.mark.linux
    def test_generic_handler_press_dpad_not_implemented(self):
        """Test that generic handler raises NotImplementedError for press_dpad."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.press_dpad("up", 0.1)

    @pytest.mark.linux
    def test_generic_handler_release_all_not_implemented(self):
        """Test that generic handler raises NotImplementedError for release_all."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            handler.release_all()

    @pytest.mark.linux
    def test_generic_handler_is_available(self):
        """Test that generic handler reports as not available."""
        handler = GamepadFactory.create_handler(force_platform="generic")

        # Generic gamepad handler should report as not available
        assert handler.is_available() is False

    @pytest.mark.linux
    def test_generic_handler_platform_name(self):
        """Test that generic handler returns correct platform name."""
        handler = GamepadFactory.create_handler(force_platform="generic")
        assert handler.get_platform_name() == "Linux/Generic"
