"""
Configuration constants and default values for the 360° Game Screenshot Automation.

This module centralizes all default values to eliminate magic numbers throughout the codebase.
All hardcoded values should be defined here and referenced by name.
"""

# Default movement configuration
DEFAULT_HORIZONTAL_STEPS = 13
DEFAULT_VERTICAL_STEPS = 6
DEFAULT_HORIZONTAL_MOVEMENT_DURATION = 0.1
DEFAULT_VERTICAL_MOVEMENT_DURATION = 0.1
DEFAULT_PAUSE_BETWEEN_MOVES = 0.3

# Default screenshot configuration
DEFAULT_SCREENSHOT_TYPE = "external_app"
DEFAULT_SCREENSHOT_KEY = "f9"
DEFAULT_SCREENSHOT_DELAY = 0.3
DEFAULT_SCREENSHOT_PAUSE = 0.3

# Default control configuration
DEFAULT_GAMEPAD_STICK_MOVEMENT = 0.8
DEFAULT_MOUSE_SENSITIVITY = 100

# Default keyboard keys
DEFAULT_KEY_LEFT = "left"
DEFAULT_KEY_RIGHT = "right"
DEFAULT_KEY_UP = "up"
DEFAULT_KEY_DOWN = "down"

# Application configuration
DEFAULT_CONFIG_VERSION = "2.0"
SUPPORTED_CONTROL_TYPES = ["keyboard", "gamepad", "mouse"]

# Timing constants
CAPTURE_COUNTDOWN_SECONDS = 5
MAX_CONFIG_LOAD_RETRIES = 3


class ConfigDefaults:
    """
    Centralized access to all default configuration values.

    This class provides a clean interface to access defaults without magic numbers.
    """

    @staticmethod
    def get_movement_defaults():
        """Get default movement configuration."""
        return {
            "horizontal_steps": DEFAULT_HORIZONTAL_STEPS,
            "vertical_steps": DEFAULT_VERTICAL_STEPS,
            "pause_between_moves": DEFAULT_PAUSE_BETWEEN_MOVES,
        }

    @staticmethod
    def get_screenshot_defaults():
        """Get default screenshot configuration."""
        return {
            "key": DEFAULT_SCREENSHOT_KEY,
            "delay": DEFAULT_SCREENSHOT_DELAY,
            "pause": DEFAULT_SCREENSHOT_PAUSE,
        }

    @staticmethod
    def get_keyboard_defaults():
        """Get default keyboard control configuration."""
        return {
            "left": DEFAULT_KEY_LEFT,
            "right": DEFAULT_KEY_RIGHT,
            "up": DEFAULT_KEY_UP,
            "down": DEFAULT_KEY_DOWN,
            "horizontal_movement_duration": DEFAULT_HORIZONTAL_MOVEMENT_DURATION,
            "vertical_movement_duration": DEFAULT_VERTICAL_MOVEMENT_DURATION,
        }

    @staticmethod
    def get_gamepad_defaults():
        """Get default gamepad control configuration."""
        return {
            "stick_movement_amount": DEFAULT_GAMEPAD_STICK_MOVEMENT,
            "horizontal_movement_duration": DEFAULT_HORIZONTAL_MOVEMENT_DURATION,
            "vertical_movement_duration": DEFAULT_VERTICAL_MOVEMENT_DURATION,
        }

    @staticmethod
    def get_mouse_defaults():
        """Get default mouse control configuration."""
        return {
            "vertical_sensitivity": DEFAULT_MOUSE_SENSITIVITY,
            "horizontal_sensitivity": DEFAULT_MOUSE_SENSITIVITY,
        }

    @staticmethod
    def get_all_control_defaults():
        """Get all control type defaults."""
        return {
            "keyboard": ConfigDefaults.get_keyboard_defaults(),
            "gamepad": ConfigDefaults.get_gamepad_defaults(),
            "mouse": ConfigDefaults.get_mouse_defaults(),
        }
