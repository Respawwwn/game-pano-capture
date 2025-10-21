"""Tests for built-in screenshot handler."""

from unittest.mock import Mock, patch

import pytest

from screenshot.built_in import BuiltInHandler


class TestBuiltInHandler:
    """Tests for built-in screenshot handler."""

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    def test_built_in_initialization_success(self):
        """Test built-in handler initializes correctly when mss is available."""
        handler = BuiltInHandler()
        # Should not raise any exceptions
        assert isinstance(handler, BuiltInHandler)

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", False)
    def test_built_in_initialization_no_mss(self):
        """Test built-in handler raises error when mss is not available."""
        with pytest.raises(ImportError, match="mss library is required"):
            BuiltInHandler()

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("time.sleep")
    def test_take_screenshot_basic_config(
        self, mock_sleep, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot with basic config."""
        # Setup mocks
        mock_exists.return_value = True
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_screenshot = Mock()
        mock_screenshot.rgb = b"fake_image_data"
        mock_screenshot.size = (1920, 1080)
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {"monitor": 1, "path": "/test/screenshots/", "pause": 0.1}
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            result = handler.take_screenshot(config)

            # Should create directory
            mock_makedirs.assert_called_once_with("/test/screenshots/", exist_ok=True)

            # Should grab screenshot from correct monitor
            mock_sct_instance.grab.assert_called_once()

            # Should save screenshot
            mock_mss.tools.to_png.assert_called_once_with(
                b"fake_image_data",
                (1920, 1080),
                output="/test/screenshots/screenshot_20231201_123456_789.png",
            )

            # Should check file exists and sleep for pause
            mock_exists.assert_called_once_with(
                "/test/screenshots/screenshot_20231201_123456_789.png"
            )
            mock_sleep.assert_called_once_with(0.1)

            # Should return file path
            assert result == "/test/screenshots/screenshot_20231201_123456_789.png"

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("time.sleep")
    def test_take_screenshot_with_delay(
        self, mock_sleep, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot with delay before screenshot."""
        # Setup mocks
        mock_exists.return_value = True
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_screenshot = Mock()
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {
                "monitor": 1,
                "path": "/test/screenshots/",
                "delay": 0.5,
                "pause": 0.2,
            }
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            result = handler.take_screenshot(config)

            # Should sleep for both delay and pause
            expected_calls = [((0.5,),), ((0.2,),)]
            assert mock_sleep.call_args_list == expected_calls

            assert result == "/test/screenshots/screenshot_20231201_123456_789.png"

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_take_screenshot_file_not_created(
        self, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot handles file creation failure."""
        # Setup mocks
        mock_exists.return_value = False  # File was not created
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_screenshot = Mock()
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {"monitor": 1, "path": "/test/screenshots/", "pause": 0.1}
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            with pytest.raises(
                Exception, match="Screenshot file was not created successfully"
            ):
                handler.take_screenshot(config)

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    def test_take_screenshot_mss_exception(self, mock_makedirs, mock_mss):
        """Test take_screenshot handles mss library exception."""
        mock_mss.mss.side_effect = RuntimeError("MSS capture error")

        handler = BuiltInHandler()

        config = {
            "screenshot": {"monitor": 1, "path": "/test/screenshots/", "pause": 0.1}
        }

        with pytest.raises(
            Exception, match="Error taking built-in screenshot: MSS capture error"
        ):
            handler.take_screenshot(config)

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_take_screenshot_invalid_monitor(
        self, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot handles invalid monitor number."""
        # Setup mocks - only one monitor available
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {
                "monitor": 2,  # Invalid - only monitor 1 exists
                "path": "/test/screenshots/",
                "pause": 0.1,
            }
        }

        with pytest.raises(Exception, match="Invalid monitor number: 2"):
            handler.take_screenshot(config)

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    def test_take_screenshot_missing_screenshot_config(self):
        """Test take_screenshot handles missing screenshot config."""
        handler = BuiltInHandler()

        config = {}  # Missing screenshot section

        with pytest.raises(Exception, match="Error taking built-in screenshot"):
            handler.take_screenshot(config)

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("time.sleep")
    def test_take_screenshot_default_values(
        self, mock_sleep, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot with default values when not specified."""
        # Setup mocks
        mock_exists.return_value = True
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_screenshot = Mock()
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {
                # No monitor, path, delay, or pause specified - should use defaults
            }
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            result = handler.take_screenshot(config)

            # Should use default monitor (1) and path (/screenshots/)
            mock_makedirs.assert_called_once_with("/screenshots/", exist_ok=True)
            mock_exists.assert_called_once_with(
                "/screenshots/screenshot_20231201_123456_789.png"
            )

            # Should use default pause (0)
            mock_sleep.assert_called_once_with(0)

            assert result == "/screenshots/screenshot_20231201_123456_789.png"

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("time.sleep")
    def test_take_screenshot_zero_pause(
        self, mock_sleep, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot with zero pause time."""
        # Setup mocks
        mock_exists.return_value = True
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,
            {"left": 0, "top": 0, "width": 1920, "height": 1080},
        ]
        mock_screenshot = Mock()
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        config = {
            "screenshot": {"monitor": 1, "path": "/test/screenshots/", "pause": 0}
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            result = handler.take_screenshot(config)

            # Should still call sleep with 0
            mock_sleep.assert_called_once_with(0)
            assert result == "/test/screenshots/screenshot_20231201_123456_789.png"

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("screenshot.built_in.mss")
    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("time.sleep")
    def test_take_screenshot_multiple_monitors(
        self, mock_sleep, mock_exists, mock_makedirs, mock_mss
    ):
        """Test take_screenshot with multiple monitors."""
        # Setup mocks with multiple monitors
        mock_exists.return_value = True
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [
            None,  # Combined monitors
            {"left": 0, "top": 0, "width": 1920, "height": 1080},  # Monitor 1
            {"left": 1920, "top": 0, "width": 1920, "height": 1080},  # Monitor 2
        ]
        mock_screenshot = Mock()
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_mss.mss.return_value.__enter__.return_value = mock_sct_instance

        handler = BuiltInHandler()

        # Test monitor 2
        config = {
            "screenshot": {"monitor": 2, "path": "/test/screenshots/", "pause": 0.1}
        }

        with patch("screenshot.built_in.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = (
                "20231201_123456_789123"
            )

            result = handler.take_screenshot(config)

            # Should grab from monitor 2
            mock_sct_instance.grab.assert_called_once_with(
                {"left": 1920, "top": 0, "width": 1920, "height": 1080}
            )
            assert result == "/test/screenshots/screenshot_20231201_123456_789.png"

    @pytest.mark.unit
    @patch("screenshot.built_in.MSS_AVAILABLE", True)
    @patch("os.makedirs")
    def test_take_screenshot_makedirs_exception(self, mock_makedirs):
        """Test take_screenshot handles directory creation failure."""
        mock_makedirs.side_effect = OSError("Permission denied")

        handler = BuiltInHandler()

        config = {
            "screenshot": {
                "monitor": 1,
                "path": "/protected/screenshots/",
                "pause": 0.1,
            }
        }

        with pytest.raises(
            Exception, match="Error taking built-in screenshot: Permission denied"
        ):
            handler.take_screenshot(config)
