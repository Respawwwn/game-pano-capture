"""Tests for external app screenshot handler."""

from unittest.mock import Mock, patch

import pytest

from screenshot.external_app import ExternalAppHandler


class TestExternalAppHandler:
    """Tests for external app screenshot handler."""

    @pytest.mark.unit
    def test_external_app_initialization(self):
        """Test external app handler initializes correctly."""
        mock_keyboard = Mock()
        handler = ExternalAppHandler(mock_keyboard)

        assert handler.keyboard_handler is mock_keyboard

    @pytest.mark.unit
    def test_take_screenshot_basic_config(self):
        """Test take_screenshot with basic config."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        config = {"screenshot": {"shortcut_key": "f9", "pause": 0.1}}

        with patch("time.sleep") as mock_sleep:
            result = handler.take_screenshot(config)

            # Should call keyboard handler with correct key
            mock_keyboard.press_key_combination.assert_called_once_with("f9")

            # Should sleep for pause duration
            mock_sleep.assert_called_once_with(0.1)

            # Should return empty string (external app handles path)
            assert result == ""

    @pytest.mark.unit
    def test_take_screenshot_with_delay(self):
        """Test take_screenshot with delay before screenshot."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        config = {
            "screenshot": {"shortcut_key": "ctrl+shift+s", "delay": 0.5, "pause": 0.2}
        }

        with patch("time.sleep") as mock_sleep:
            result = handler.take_screenshot(config)

            # Should call keyboard handler
            mock_keyboard.press_key_combination.assert_called_once_with("ctrl+shift+s")

            # Should sleep for both delay and pause
            expected_calls = [((0.5,),), ((0.2,),)]
            assert mock_sleep.call_args_list == expected_calls

            assert result == ""

    @pytest.mark.unit
    def test_take_screenshot_keyboard_failure(self):
        """Test take_screenshot handles keyboard handler failure."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = False
        handler = ExternalAppHandler(mock_keyboard)

        config = {"screenshot": {"shortcut_key": "f9", "pause": 0.1}}

        with pytest.raises(
            Exception, match="Failed to trigger screenshot key combination"
        ):
            handler.take_screenshot(config)

    @pytest.mark.unit
    def test_take_screenshot_keyboard_exception(self):
        """Test take_screenshot handles keyboard handler exception."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.side_effect = RuntimeError("Keyboard error")
        handler = ExternalAppHandler(mock_keyboard)

        config = {"screenshot": {"shortcut_key": "f9", "pause": 0.1}}

        with pytest.raises(
            Exception, match="Error triggering screenshot: Keyboard error"
        ):
            handler.take_screenshot(config)

    @pytest.mark.unit
    def test_take_screenshot_missing_screenshot_config(self):
        """Test take_screenshot handles missing screenshot config."""
        mock_keyboard = Mock()
        handler = ExternalAppHandler(mock_keyboard)

        config = {}  # Missing screenshot section

        with pytest.raises(Exception, match="Error triggering screenshot"):
            handler.take_screenshot(config)

    @pytest.mark.unit
    def test_take_screenshot_missing_shortcut_key(self):
        """Test take_screenshot handles missing shortcut_key."""
        mock_keyboard = Mock()
        handler = ExternalAppHandler(mock_keyboard)

        config = {
            "screenshot": {
                "pause": 0.1
                # Missing shortcut_key
            }
        }

        with pytest.raises(Exception, match="Error triggering screenshot"):
            handler.take_screenshot(config)

    @pytest.mark.unit
    def test_take_screenshot_zero_pause(self):
        """Test take_screenshot with zero pause time."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        config = {"screenshot": {"shortcut_key": "f9", "pause": 0}}

        with patch("time.sleep") as mock_sleep:
            result = handler.take_screenshot(config)

            # Should still call sleep with 0
            mock_sleep.assert_called_once_with(0)
            assert result == ""

    @pytest.mark.unit
    def test_take_screenshot_default_pause(self):
        """Test take_screenshot with default pause when not specified."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        config = {
            "screenshot": {
                "shortcut_key": "f9"
                # No pause specified - should default to 0
            }
        }

        with patch("time.sleep") as mock_sleep:
            result = handler.take_screenshot(config)

            # Should use default pause of 0
            mock_sleep.assert_called_once_with(0)
            assert result == ""

    @pytest.mark.unit
    def test_take_screenshot_default_delay(self):
        """Test take_screenshot with default delay when not specified."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        config = {
            "screenshot": {
                "shortcut_key": "f9",
                "pause": 0.1,
                # No delay specified - should default to 0
            }
        }

        with patch("time.sleep") as mock_sleep:
            result = handler.take_screenshot(config)

            # Should only sleep for pause, not delay
            mock_sleep.assert_called_once_with(0.1)
            assert result == ""

    @pytest.mark.unit
    def test_take_screenshot_complex_key_combination(self):
        """Test take_screenshot with complex key combinations."""
        mock_keyboard = Mock()
        mock_keyboard.press_key_combination.return_value = True
        handler = ExternalAppHandler(mock_keyboard)

        complex_keys = [
            "ctrl+shift+alt+f12",
            "cmd+shift+4",
            "win+printscreen",
            "ctrl+alt+delete",
        ]

        for key_combo in complex_keys:
            config = {"screenshot": {"shortcut_key": key_combo, "pause": 0.1}}

            with patch("time.sleep"):
                result = handler.take_screenshot(config)

                mock_keyboard.press_key_combination.assert_called_with(key_combo)
                assert result == ""

            # Reset mock for next iteration
            mock_keyboard.reset_mock()
