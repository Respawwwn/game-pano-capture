from .built_in import BuiltInHandler
from .external_app import ExternalAppHandler
from .interface import ScreenshotHandler


def create_handler(screenshot_type: str, keyboard_handler=None) -> ScreenshotHandler:
    """Create a screenshot handler based on the specified type.

    Args:
        screenshot_type: Type of screenshot handler ("external_app" or "built_in")
        keyboard_handler: Keyboard handler instance (required for external_app)

    Returns:
        ScreenshotHandler: Appropriate screenshot handler instance

    Raises:
        ValueError: If screenshot_type is not supported
        TypeError: If required dependencies are missing
    """
    if screenshot_type == "external_app":
        if keyboard_handler is None:
            raise ValueError(
                "keyboard_handler is required for external_app screenshot type"
            )
        return ExternalAppHandler(keyboard_handler)

    elif screenshot_type == "built_in":
        return BuiltInHandler()

    else:
        raise ValueError(
            f"Unsupported screenshot type: {screenshot_type}. "
            f"Supported types: 'external_app', 'built_in'"
        )
