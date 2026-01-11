"""
macOS-specific mouse handler implementation using Quartz and PyObjC.

This handler provides native macOS mouse control using the Quartz framework
for optimal compatibility with games and applications.
"""

import logging

from .interface import IMouseHandler

try:
    import Quartz
    from Quartz import (
        CGEventCreateMouseEvent,
        CGEventCreateScrollWheelEvent,
        CGEventGetLocation,
        CGEventPost,
        CGEventSourceCreate,
        kCGEventLeftMouseDown,
        kCGEventLeftMouseUp,
        kCGEventMouseMoved,
        kCGEventOtherMouseDown,
        kCGEventOtherMouseUp,
        kCGEventRightMouseDown,
        kCGEventRightMouseUp,
        kCGEventSourceStateHIDSystemState,
        kCGHIDEventTap,
    )

    QUARTZ_AVAILABLE = True
except ImportError:
    QUARTZ_AVAILABLE = False
    Quartz = None


class MacOSMouseHandler(IMouseHandler):
    """
    macOS-specific mouse handler using Quartz Core Graphics.

    This implementation uses the native macOS Quartz framework for mouse control,
    providing excellent compatibility with games and applications.
    """

    def __init__(self):
        """Initialize the macOS mouse handler."""
        self._logger = logging.getLogger(__name__)

        if not QUARTZ_AVAILABLE:
            self._logger.warning("Quartz (PyObjC) not available for mouse control")
            return

        try:
            # Create event source for generating mouse events
            self._event_source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
            self._logger.info("macOS Quartz mouse handler initialized")
        except Exception as e:
            self._logger.error(f"Failed to initialize Quartz event source: {e}")
            self._event_source = None

    def move_relative(self, dx: int, dy: int) -> bool:
        """
        Move the mouse cursor by relative amounts using Quartz.

        Args:
            dx: Horizontal movement in pixels (positive = right, negative = left)
            dy: Vertical movement in pixels (positive = down, negative = up)

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        try:
            # Get current mouse position
            current_x, current_y = self.get_position()
            new_x = current_x + dx
            new_y = current_y + dy

            # Create and post mouse move event
            mouse_event = CGEventCreateMouseEvent(
                self._event_source,
                kCGEventMouseMoved,
                (new_x, new_y),
                0,  # button number (not used for mouse move)
            )

            CGEventPost(kCGHIDEventTap, mouse_event)

            self._logger.debug(
                f"Moved mouse relatively by ({dx}, {dy}) to ({new_x}, {new_y})"
            )
            return True

        except Exception as e:
            self._logger.error(f"Failed to move mouse relatively: {e}")
            return False

    def move_absolute(self, x: int, y: int) -> bool:
        """
        Move the mouse cursor to absolute screen coordinates.

        Args:
            x: Horizontal position in pixels
            y: Vertical position in pixels

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        try:
            # Create and post mouse move event
            mouse_event = CGEventCreateMouseEvent(
                self._event_source,
                kCGEventMouseMoved,
                (x, y),
                0,  # button number (not used for mouse move)
            )

            CGEventPost(kCGHIDEventTap, mouse_event)

            self._logger.debug(f"Moved mouse to absolute position ({x}, {y})")
            return True

        except Exception as e:
            self._logger.error(f"Failed to move mouse to absolute position: {e}")
            return False

    def get_position(self) -> tuple[int, int]:
        """
        Get the current mouse cursor position.

        Returns:
            Tuple of (x, y) coordinates in pixels
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return (0, 0)

        try:
            # Create a dummy event to get current mouse position
            dummy_event = CGEventCreateMouseEvent(
                self._event_source, kCGEventMouseMoved, (0, 0), 0
            )

            location = CGEventGetLocation(dummy_event)
            x, y = int(location.x), int(location.y)

            self._logger.debug(f"Current mouse position: ({x}, {y})")
            return (x, y)

        except Exception as e:
            self._logger.error(f"Failed to get mouse position: {e}")
            return (0, 0)

    def click(self, button: str = "left") -> bool:
        """
        Click a mouse button using Quartz events.

        Args:
            button: Mouse button to click ('left', 'right', 'middle')

        Returns:
            True if successful, False otherwise
        """
        # Use press and release for consistent behavior
        if not self.press(button):
            return False
        return self.release(button)

    def press(self, button: str = "left") -> bool:
        """
        Press and hold a mouse button without releasing.

        Args:
            button: Mouse button to press ('left', 'right', 'middle')

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        button_events = {
            "left": (kCGEventLeftMouseDown, kCGEventLeftMouseUp, 0),
            "right": (kCGEventRightMouseDown, kCGEventRightMouseUp, 1),
            "middle": (kCGEventOtherMouseDown, kCGEventOtherMouseUp, 2),
        }

        button_config = button_events.get(button.lower())
        if button_config is None:
            self._logger.error(f"Invalid button: {button}")
            return False

        down_event, up_event, button_num = button_config

        try:
            # Get current mouse position
            x, y = self.get_position()

            # Create and post mouse down event
            mouse_down = CGEventCreateMouseEvent(
                self._event_source, down_event, (x, y), button_num
            )
            CGEventPost(kCGHIDEventTap, mouse_down)

            self._logger.debug(f"Pressed {button} mouse button")
            return True

        except Exception as e:
            self._logger.error(f"Failed to press mouse button: {e}")
            return False

    def release(self, button: str = "left") -> bool:
        """
        Release a previously pressed mouse button.

        Args:
            button: Mouse button to release ('left', 'right', 'middle')

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        button_events = {
            "left": (kCGEventLeftMouseDown, kCGEventLeftMouseUp, 0),
            "right": (kCGEventRightMouseDown, kCGEventRightMouseUp, 1),
            "middle": (kCGEventOtherMouseDown, kCGEventOtherMouseUp, 2),
        }

        button_config = button_events.get(button.lower())
        if button_config is None:
            self._logger.error(f"Invalid button: {button}")
            return False

        down_event, up_event, button_num = button_config

        try:
            # Get current mouse position
            x, y = self.get_position()

            # Create and post mouse up event
            mouse_up = CGEventCreateMouseEvent(
                self._event_source, up_event, (x, y), button_num
            )
            CGEventPost(kCGHIDEventTap, mouse_up)

            self._logger.debug(f"Released {button} mouse button")
            return True

        except Exception as e:
            self._logger.error(f"Failed to release mouse button: {e}")
            return False

    def scroll(self, dx: int = 0, dy: int = 0) -> bool:
        """
        Scroll the mouse wheel using Quartz scroll events.

        Args:
            dx: Horizontal scroll amount (positive = right, negative = left)
            dy: Vertical scroll amount (positive = up, negative = down)

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        try:
            # Create scroll wheel event
            scroll_event = CGEventCreateScrollWheelEvent(
                self._event_source,
                2,  # Number of scroll wheel axes (vertical and horizontal)
                dy,  # Vertical scroll
                dx,  # Horizontal scroll
            )

            CGEventPost(kCGHIDEventTap, scroll_event)

            self._logger.debug(f"Scrolled mouse wheel (dx={dx}, dy={dy})")
            return True

        except Exception as e:
            self._logger.error(f"Failed to scroll mouse wheel: {e}")
            return False

    def is_available(self) -> bool:
        """
        Check if the mouse handler is available and properly initialized.

        Returns:
            True if the handler is available and can be used, False otherwise
        """
        return QUARTZ_AVAILABLE and self._event_source is not None

    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.

        Returns:
            Platform name as a string
        """
        return "macOS"
