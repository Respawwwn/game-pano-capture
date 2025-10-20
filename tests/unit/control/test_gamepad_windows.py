"""Tests specific to Windows gamepad handler."""

from unittest.mock import Mock, patch

import pytest

from control.gamepad.factory import GamepadFactory


class TestGamepadWindows:
    """Tests specific to Windows gamepad handler."""

    @pytest.mark.windows
    def test_windows_handler_initialization(self):
        """Test Windows handler initializes correctly."""
        handler = GamepadFactory.create_handler(force_platform="windows")
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_handler_with_vgamepad_available(self):
        """Test Windows handler when vgamepad is available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg:
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")

            # Initialize should succeed with vgamepad available
            result = handler.initialize()
            assert result is True
            assert mock_vg.VX360Gamepad.called

    @pytest.mark.windows
    def test_windows_handler_without_vgamepad(self):
        """Test Windows handler when vgamepad is not available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # Initialize should fail without vgamepad
            result = handler.initialize()
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_move_stick_with_vgamepad(self):
        """Test Windows handler move_stick with vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg, patch("time.sleep"):
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test move_stick
            result = handler.move_stick("right", 0.5, 0.0, 0.1)
            assert result is True
            assert mock_gamepad.right_joystick_float.called
            assert mock_gamepad.update.called

    @pytest.mark.windows
    def test_windows_handler_move_stick_without_vgamepad(self):
        """Test Windows handler move_stick without vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # move_stick should fail without vgamepad
            result = handler.move_stick("right", 0.5, 0.0, 0.1)
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_press_button_with_vgamepad(self):
        """Test Windows handler press_button with vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg, patch("time.sleep"):
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test press_button
            result = handler.press_button("a", 0.1)
            assert result is True
            assert mock_gamepad.press_button.called
            assert mock_gamepad.release_button.called
            assert mock_gamepad.update.call_count >= 2

    @pytest.mark.windows
    def test_windows_handler_press_button_without_vgamepad(self):
        """Test Windows handler press_button without vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # press_button should fail without vgamepad
            result = handler.press_button("a", 0.1)
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_press_trigger_with_vgamepad(self):
        """Test Windows handler press_trigger with vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg, patch("time.sleep"):
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test press_trigger
            result = handler.press_trigger("right", 0.5, 0.1)
            assert result is True
            assert mock_gamepad.right_trigger_float.called
            assert mock_gamepad.update.called

    @pytest.mark.windows
    def test_windows_handler_press_trigger_without_vgamepad(self):
        """Test Windows handler press_trigger without vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # press_trigger should fail without vgamepad
            result = handler.press_trigger("right", 0.5, 0.1)
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_press_dpad_with_vgamepad(self):
        """Test Windows handler press_dpad with vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg, patch("time.sleep"):
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test press_dpad
            result = handler.press_dpad("up", 0.1)
            assert result is True
            assert mock_gamepad.press_button.called
            assert mock_gamepad.release_button.called
            assert mock_gamepad.update.call_count >= 2

    @pytest.mark.windows
    def test_windows_handler_press_dpad_without_vgamepad(self):
        """Test Windows handler press_dpad without vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # press_dpad should fail without vgamepad
            result = handler.press_dpad("up", 0.1)
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_release_all_with_vgamepad(self):
        """Test Windows handler release_all with vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg:
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test release_all
            result = handler.release_all()
            assert result is True
            assert mock_gamepad.reset.called
            assert mock_gamepad.update.called

    @pytest.mark.windows
    def test_windows_handler_release_all_without_vgamepad(self):
        """Test Windows handler release_all without vgamepad available."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # release_all should fail without vgamepad
            result = handler.release_all()
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_is_available_with_vgamepad(self):
        """Test Windows handler availability with vgamepad."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # Should be available with vgamepad
            assert handler.is_available() is True

    @pytest.mark.windows
    def test_windows_handler_is_available_without_vgamepad(self):
        """Test Windows handler availability without vgamepad."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", False):
            handler = GamepadFactory.create_handler(force_platform="windows")

            # Should not be available without vgamepad
            assert handler.is_available() is False

    @pytest.mark.windows
    def test_windows_handler_platform_name(self):
        """Test that Windows handler returns correct platform name."""
        handler = GamepadFactory.create_handler(force_platform="windows")
        assert handler.get_platform_name() == "Windows"

    @pytest.mark.windows
    def test_windows_handler_stick_validation(self):
        """Test that Windows handler validates stick names."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg:
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test valid stick names
            result = handler.move_stick("left", 0.5, 0.0, 0.1)
            assert result is True

            result = handler.move_stick("right", 0.5, 0.0, 0.1)
            assert result is True

            # Test invalid stick name
            result = handler.move_stick("invalid", 0.5, 0.0, 0.1)
            assert result is False

    @pytest.mark.windows
    def test_windows_handler_button_validation(self):
        """Test that Windows handler validates button names."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg:
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test valid buttons
            valid_buttons = ["a", "b", "x", "y", "start", "select"]
            for button in valid_buttons:
                result = handler.press_button(button, 0.1)
                assert result is True

    @pytest.mark.windows
    def test_windows_handler_trigger_validation(self):
        """Test that Windows handler validates trigger names."""
        with patch("control.gamepad.windows.VGAMEPAD_AVAILABLE", True), patch(
            "control.gamepad.windows.vg"
        ) as mock_vg:
            mock_gamepad = Mock()
            mock_vg.VX360Gamepad.return_value = mock_gamepad

            handler = GamepadFactory.create_handler(force_platform="windows")
            handler.initialize()

            # Test valid triggers
            result = handler.press_trigger("left", 0.5, 0.1)
            assert result is True

            result = handler.press_trigger("right", 0.5, 0.1)
            assert result is True

            # Test invalid trigger name
            result = handler.press_trigger("invalid", 0.5, 0.1)
            assert result is False
