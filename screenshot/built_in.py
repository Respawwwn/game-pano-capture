import os
import time
from datetime import datetime

from .interface import ScreenshotHandler

try:
    import mss

    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

try:
    import importlib.util

    PIL_AVAILABLE = importlib.util.find_spec("PIL.Image") is not None
except ImportError:
    PIL_AVAILABLE = False


class BuiltInHandler(ScreenshotHandler):
    def __init__(self):
        if not MSS_AVAILABLE:
            raise ImportError(
                "mss library is required for built-in screenshots. Install with: pip install mss"
            )

    def take_screenshot(self, config: dict) -> str:
        """Take screenshot directly using built-in functionality.

        Args:
            config: Screenshot configuration dictionary containing:
                - monitor: Monitor number to capture (1-based index)
                - path: Directory path to save screenshots
                - pause: Wait time after taking screenshot (optional)
                - delay: Wait time before taking screenshot (optional)

        Returns:
            str: Path to the saved screenshot file

        Raises:
            Exception: If screenshot capture fails
        """
        try:
            screenshot_config = config["screenshot"]
            monitor_num = screenshot_config.get("monitor", 1)
            save_path = screenshot_config.get("path", "/screenshots/")
            delay = screenshot_config.get("delay", 0)
            pause = screenshot_config.get("pause", 0)

            # Ensure save directory exists
            os.makedirs(save_path, exist_ok=True)

            # Wait before taking screenshot if specified
            if delay > 0:
                time.sleep(delay)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(save_path, filename)

            # Take screenshot using mss
            with mss.mss() as sct:
                # Get monitor info (mss uses 0-based indexing, but config uses 1-based)
                monitors = sct.monitors
                if monitor_num < 1 or monitor_num > len(monitors) - 1:
                    raise Exception(
                        f"Invalid monitor number: {monitor_num}. Available monitors: 1-{len(monitors) - 1}"
                    )

                monitor = monitors[monitor_num]  # monitors[0] is all monitors combined

                # Capture screenshot
                screenshot = sct.grab(monitor)

                # Save screenshot
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)

            # Verify file was created successfully
            if os.path.exists(filepath):
                # Wait for screenshot to be processed
                time.sleep(pause)
                return filepath
            else:
                raise Exception("Screenshot file was not created successfully")

        except Exception as e:
            raise Exception(f"Error taking built-in screenshot: {e}") from e
