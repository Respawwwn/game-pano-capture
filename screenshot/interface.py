from abc import ABC, abstractmethod


class ScreenshotHandler(ABC):
    @abstractmethod
    def take_screenshot(self, config: dict) -> str:
        """Take a screenshot and return the path to the saved image.

        Args:
            config: Screenshot configuration dictionary

        Returns:
            str: Path to the saved screenshot file

        Raises:
            Exception: If screenshot capture fails
        """
