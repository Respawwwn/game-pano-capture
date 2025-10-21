import time

from .interface import ScreenshotHandler


class ExternalAppHandler(ScreenshotHandler):
    def __init__(self, keyboard_handler):
        self.keyboard_handler = keyboard_handler

    def take_screenshot(self, config: dict) -> str:
        """Trigger screenshot using external application via keyboard shortcut.

        Args:
            config: Screenshot configuration dictionary containing:
                - shortcut_key: Key combination for screenshot tool
                - pause: Wait time after taking screenshot (optional)
                - delay: Wait time before taking screenshot (optional)

        Returns:
            str: Empty string (external app handles file path)

        Raises:
            Exception: If screenshot trigger fails
        """
        try:
            screenshot_config = config["screenshot"]
            screenshot_key = screenshot_config["shortcut_key"]
            delay = screenshot_config.get("delay", 0)
            pause = screenshot_config.get("pause", 0)

            # Wait before taking screenshot if specified
            if delay > 0:
                time.sleep(delay)

            # Use platform-specific keyboard handler
            success = self.keyboard_handler.press_key_combination(screenshot_key)

            if success:
                # Wait for screenshot to be processed by external tool
                time.sleep(pause)
                return ""  # External app handles file path
            else:
                raise Exception("Failed to trigger screenshot key combination")

        except Exception as e:
            raise Exception(f"Error triggering screenshot: {e}") from e
