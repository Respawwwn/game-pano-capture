"""
Generic mouse handler implementation using pygame.

This handler works on most Linux systems and serves as a fallback
for platforms without specialized implementations.
"""

import logging

from .interface import IMouseHandler

try:
    import pygame

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None


class GenericMouseHandler(IMouseHandler):
    """
    Generic mouse handler using pygame for cross-platform compatibility.

    This implementation uses pygame for mouse control, which works on most
    platforms but may have limitations with game interaction.
    """

    def __init__(self):
        """Initialize the generic mouse handler."""
        self._pygame_initialized = False
        self._logger = logging.getLogger(__name__)

        if not PYGAME_AVAILABLE:
            self._logger.warning("pygame not available for mouse control")
            return

        try:
            pygame.init()
            self._pygame_initialized = True
            self._logger.info("pygame initialized for mouse control")
        except Exception as e:
            self._logger.error(f"Failed to initialize pygame: {e}")
            self._pygame_initialized = False

    def move_relative(self, dx: int, dy: int) -> bool:
        """
        Move the mouse cursor by relative amounts using pygame.

        Note: This uses absolute positioning as pygame doesn't support
        true relative movement. This may not work properly in games.

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
            current_pos = pygame.mouse.get_pos()
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy

            pygame.mouse.set_pos((new_x, new_y))
            pygame.event.pump()

            self._logger.debug(f"Moved mouse from {current_pos} to ({new_x}, {new_y})")
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
            pygame.mouse.set_pos((x, y))
            pygame.event.pump()

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
            pos = pygame.mouse.get_pos()
            self._logger.debug(f"Current mouse position: {pos}")
            return pos

        except Exception as e:
            self._logger.error(f"Failed to get mouse position: {e}")
            return (0, 0)

    def click(self, button: str = "left") -> bool:
        """
        Click a mouse button.

        Note: pygame mouse clicks may not work in all applications,
        especially games that use low-level input.

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

        button_map = {"left": 1, "middle": 2, "right": 3}

        button_id = button_map.get(button.lower())
        if button_id is None:
            self._logger.error(f"Invalid button: {button}")
            return False

        try:
            # Generate mouse down event
            pygame.event.post(
                pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": button_id})
            )
            pygame.event.pump()

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

        button_map = {"left": 1, "middle": 2, "right": 3}

        button_id = button_map.get(button.lower())
        if button_id is None:
            self._logger.error(f"Invalid button: {button}")
            return False

        try:
            # Generate mouse up event
            pygame.event.post(
                pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": button_id})
            )
            pygame.event.pump()

            self._logger.debug(f"Released {button} mouse button")
            return True

        except Exception as e:
            self._logger.error(f"Failed to release mouse button: {e}")
            return False

    def scroll(self, dx: int = 0, dy: int = 0) -> bool:
        """
        Scroll the mouse wheel.

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
            # Generate scroll events
            if dy != 0:
                pygame.event.post(
                    pygame.event.Event(pygame.MOUSEWHEEL, {"y": dy, "x": dx})
                )
                pygame.event.pump()

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
        return PYGAME_AVAILABLE and self._pygame_initialized

    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.

        Returns:
            Platform name as a string
        """
        return "Linux/Generic"
