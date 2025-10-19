"""
Windows-specific mouse handler implementation using win32api and ctypes.

This handler provides native Windows mouse control using win32api
for optimal compatibility with games and applications.
"""

import logging

from .interface import IMouseHandler

try:
    import win32api
    import win32con
    import win32gui

    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    win32api = None
    win32con = None
    win32gui = None

try:
    import ctypes
    from ctypes import wintypes

    CTYPES_AVAILABLE = True
except ImportError:
    CTYPES_AVAILABLE = False
    ctypes = None


class WindowsMouseHandler(IMouseHandler):
    """
    Windows-specific mouse handler using win32api and ctypes.

    This implementation uses native Windows APIs for mouse control,
    providing excellent compatibility with games and applications.
    """

    def __init__(self):
        """Initialize the Windows mouse handler."""
        self._logger = logging.getLogger(__name__)

        if not WIN32_AVAILABLE and not CTYPES_AVAILABLE:
            self._logger.warning(
                "Neither win32api nor ctypes available for mouse control"
            )
            return

        if WIN32_AVAILABLE:
            self._logger.info("Windows mouse handler initialized with win32api")
        elif CTYPES_AVAILABLE:
            self._logger.info("Windows mouse handler initialized with ctypes")

    def move_relative(self, dx: int, dy: int) -> bool:
        """
        Move the mouse cursor by relative amounts using Windows APIs.

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
            if WIN32_AVAILABLE:
                # Use win32api for relative mouse movement
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
                self._logger.debug(
                    f"Moved mouse relatively by ({dx}, {dy}) using win32api"
                )
                return True
            elif CTYPES_AVAILABLE:
                # Use ctypes with SendInput for relative movement
                # This is more reliable for games
                user32 = ctypes.windll.user32

                # Define INPUT structure
                class POINT(ctypes.Structure):
                    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

                class MOUSEINPUT(ctypes.Structure):
                    _fields_ = [
                        ("dx", ctypes.c_long),
                        ("dy", ctypes.c_long),
                        ("mouseData", wintypes.DWORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
                    ]

                class INPUT(ctypes.Structure):
                    class _INPUT(ctypes.Union):
                        _fields_ = [("mi", MOUSEINPUT)]

                    _anonymous_ = ("_input",)
                    _fields_ = [("type", wintypes.DWORD), ("_input", _INPUT)]

                # Create input structure for relative movement
                extra = ctypes.c_ulong(0)
                ii_ = INPUT()
                ii_.type = 0  # INPUT_MOUSE
                ii_.mi.dx = dx
                ii_.mi.dy = dy
                ii_.mi.mouseData = 0
                ii_.mi.dwFlags = 0x0001  # MOUSEEVENTF_MOVE
                ii_.mi.time = 0
                ii_.mi.dwExtraInfo = ctypes.pointer(extra)

                # Send the input
                user32.SendInput(1, ctypes.byref(ii_), ctypes.sizeof(INPUT))
                self._logger.debug(
                    f"Moved mouse relatively by ({dx}, {dy}) using ctypes"
                )
                return True
            else:
                return False

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
            if WIN32_AVAILABLE:
                # Use win32api for absolute positioning
                win32api.SetCursorPos((x, y))
                self._logger.debug(
                    f"Moved mouse to absolute position ({x}, {y}) using win32api"
                )
                return True
            elif CTYPES_AVAILABLE:
                # Use ctypes for absolute positioning
                ctypes.windll.user32.SetCursorPos(x, y)
                self._logger.debug(
                    f"Moved mouse to absolute position ({x}, {y}) using ctypes"
                )
                return True
            else:
                return False

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
            if WIN32_AVAILABLE:
                x, y = win32api.GetCursorPos()
                self._logger.debug(f"Current mouse position: ({x}, {y}) via win32api")
                return (x, y)
            elif CTYPES_AVAILABLE:
                point = ctypes.wintypes.POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                self._logger.debug(
                    f"Current mouse position: ({point.x}, {point.y}) via ctypes"
                )
                return (point.x, point.y)
            else:
                return (0, 0)

        except Exception as e:
            self._logger.error(f"Failed to get mouse position: {e}")
            return (0, 0)

    def click(self, button: str = "left") -> bool:
        """
        Click a mouse button using Windows APIs.

        Args:
            button: Mouse button to click ('left', 'right', 'middle')

        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Mouse handler not available")
            return False

        if WIN32_AVAILABLE:
            button_events = {
                "left": (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
                "right": (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
                "middle": (
                    win32con.MOUSEEVENTF_MIDDLEDOWN,
                    win32con.MOUSEEVENTF_MIDDLEUP,
                ),
            }
        else:
            # ctypes constants
            button_events = {
                "left": (0x0002, 0x0004),  # MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
                "right": (0x0008, 0x0010),  # MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
                "middle": (
                    0x0020,
                    0x0040,
                ),  # MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
            }

        button_config = button_events.get(button.lower())
        if button_config is None:
            self._logger.error(f"Invalid button: {button}")
            return False

        down_event, up_event = button_config

        try:
            if WIN32_AVAILABLE:
                # Use win32api for mouse click
                win32api.mouse_event(down_event, 0, 0, 0, 0)
                win32api.mouse_event(up_event, 0, 0, 0, 0)
                self._logger.debug(f"Clicked {button} mouse button using win32api")
                return True
            elif CTYPES_AVAILABLE:
                # Use ctypes for mouse click
                ctypes.windll.user32.mouse_event(down_event, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(up_event, 0, 0, 0, 0)
                self._logger.debug(f"Clicked {button} mouse button using ctypes")
                return True
            else:
                return False

        except Exception as e:
            self._logger.error(f"Failed to click mouse button: {e}")
            return False

    def scroll(self, dx: int = 0, dy: int = 0) -> bool:
        """
        Scroll the mouse wheel using Windows APIs.

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
            # Convert scroll amounts to Windows wheel delta (120 units per notch)
            wheel_delta_y = dy * 120
            wheel_delta_x = dx * 120

            if WIN32_AVAILABLE:
                # Vertical scroll
                if dy != 0:
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_WHEEL, 0, 0, wheel_delta_y, 0
                    )
                # Horizontal scroll
                if dx != 0:
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_HWHEEL, 0, 0, wheel_delta_x, 0
                    )
                self._logger.debug(
                    f"Scrolled mouse wheel (dx={dx}, dy={dy}) using win32api"
                )
                return True
            elif CTYPES_AVAILABLE:
                # Vertical scroll
                if dy != 0:
                    ctypes.windll.user32.mouse_event(
                        0x0800, 0, 0, wheel_delta_y, 0
                    )  # MOUSEEVENTF_WHEEL
                # Horizontal scroll
                if dx != 0:
                    ctypes.windll.user32.mouse_event(
                        0x01000, 0, 0, wheel_delta_x, 0
                    )  # MOUSEEVENTF_HWHEEL
                self._logger.debug(
                    f"Scrolled mouse wheel (dx={dx}, dy={dy}) using ctypes"
                )
                return True
            else:
                return False

        except Exception as e:
            self._logger.error(f"Failed to scroll mouse wheel: {e}")
            return False

    def is_available(self) -> bool:
        """
        Check if the mouse handler is available and properly initialized.

        Returns:
            True if the handler is available and can be used, False otherwise
        """
        return WIN32_AVAILABLE or CTYPES_AVAILABLE

    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.

        Returns:
            Platform name as a string
        """
        return "Windows"
