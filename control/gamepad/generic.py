"""
Generic gamepad handler implementation for Linux.

This handler provides a placeholder implementation for Linux systems
where gamepad support is not currently implemented.
"""

import logging

from .interface import IGamepadHandler


class GenericGamepadHandler(IGamepadHandler):
    """
    Generic gamepad handler for Linux systems.

    This implementation currently does not provide actual gamepad functionality
    and will raise exceptions indicating that gamepad support is not available
    on this platform.
    """

    def __init__(self):
        """Initialize the generic gamepad handler."""
        self._logger = logging.getLogger(__name__)
        self._logger.info("Generic gamepad handler initialized (Linux)")

    def initialize(self) -> bool:
        """
        Initialize the gamepad handler.

        Returns:
            False as gamepad is not supported on Linux

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad support is not implemented for Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def move_stick(
        self, stick: str, x_value: float, y_value: float, duration: float
    ) -> bool:
        """
        Move a gamepad stick to specified position for a duration.

        Args:
            stick: Stick to move ('left', 'right')
            x_value: X-axis value (-1.0 to 1.0)
            y_value: Y-axis value (-1.0 to 1.0)
            duration: How long to hold the position in seconds

        Returns:
            False as gamepad is not supported

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad stick movement is not supported on Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def press_button(self, button: str, duration: float = 0.1) -> bool:
        """
        Press a gamepad button for specified duration.

        Args:
            button: Button to press
            duration: How long to hold the button in seconds

        Returns:
            False as gamepad is not supported

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad button press is not supported on Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def press_trigger(self, trigger: str, value: float, duration: float = 0.1) -> bool:
        """
        Press a gamepad trigger with specified intensity.

        Args:
            trigger: Trigger to press ('left', 'right')
            value: Trigger value (0.0 to 1.0)
            duration: How long to hold the trigger in seconds

        Returns:
            False as gamepad is not supported

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad trigger press is not supported on Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def press_dpad(self, direction: str, duration: float = 0.1) -> bool:
        """
        Press a directional pad direction.

        Args:
            direction: Direction to press ('up', 'down', 'left', 'right')
            duration: How long to hold the direction in seconds

        Returns:
            False as gamepad is not supported

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad D-pad press is not supported on Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def release_all(self) -> bool:
        """
        Release all buttons, sticks, and triggers.

        Returns:
            False as gamepad is not supported

        Raises:
            NotImplementedError: Gamepad not supported on Linux
        """
        self._logger.error("Gamepad release is not supported on Linux")
        raise NotImplementedError("Gamepad support is not available for Linux platform")

    def is_available(self) -> bool:
        """
        Check if the gamepad handler is available.

        Returns:
            False as gamepad is not supported on Linux
        """
        return False

    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.

        Returns:
            Platform name as a string
        """
        return "Linux/Generic"
