"""
macOS-specific keyboard implementation using Quartz (Core Graphics).
"""

import time
from typing import List

from .interface import IKeyboardHandler


class MacOSKeyboardHandler(IKeyboardHandler):
    """macOS keyboard handler using Quartz/Core Graphics."""

    def __init__(self):
        self._key_codes = {
            "left": 123,
            "right": 124,
            "up": 126,
            "down": 125,
            "a": 0,
            "b": 11,
            "c": 8,
            "d": 2,
            "e": 14,
            "f": 3,
            "g": 5,
            "h": 4,
            "i": 34,
            "j": 38,
            "k": 40,
            "l": 37,
            "m": 46,
            "n": 45,
            "o": 31,
            "p": 35,
            "q": 12,
            "r": 15,
            "s": 1,
            "t": 17,
            "u": 32,
            "v": 9,
            "w": 13,
            "x": 7,
            "y": 16,
            "z": 6,
            "1": 18,
            "2": 19,
            "3": 20,
            "4": 21,
            "5": 23,
            "6": 22,
            "7": 26,
            "8": 28,
            "9": 25,
            "0": 29,
            "f1": 122,
            "f2": 120,
            "f3": 99,
            "f4": 118,
            "f5": 96,
            "f6": 97,
            "f7": 98,
            "f8": 100,
            "f9": 101,
            "f10": 109,
            "f11": 103,
            "f12": 111,
            "space": 49,
            "enter": 36,
            "tab": 48,
            "shift": 56,
            "cmd": 55,
            "ctrl": 59,
            "alt": 58,
            "option": 58,
            "escape": 53,
            "delete": 51,
        }

        # Try to import and cache Quartz components
        self._quartz_available = False
        self._cgEvent = None
        self._cgPost = None
        self._cgHIDEventTap = None
        self._cgSetFlags = None
        self._modifier_masks = {}

        self._initialize_quartz()

    def _initialize_quartz(self):
        """Initialize Quartz components if available."""
        try:
            from Quartz import (
                CGEventCreateKeyboardEvent,
                CGEventPost,
                CGEventSetFlags,
                kCGEventFlagMaskAlternate,
                kCGEventFlagMaskCommand,
                kCGEventFlagMaskControl,
                kCGEventFlagMaskShift,
                kCGHIDEventTap,
            )

            self._cgEvent = CGEventCreateKeyboardEvent
            self._cgPost = CGEventPost
            self._cgHIDEventTap = kCGHIDEventTap
            self._cgSetFlags = CGEventSetFlags

            self._modifier_masks = {
                "cmd": kCGEventFlagMaskCommand,
                "command": kCGEventFlagMaskCommand,
                "shift": kCGEventFlagMaskShift,
                "ctrl": kCGEventFlagMaskControl,
                "control": kCGEventFlagMaskControl,
                "alt": kCGEventFlagMaskAlternate,
                "option": kCGEventFlagMaskAlternate,
            }

            self._quartz_available = True
            print("macOS: Quartz keyboard handler initialized")

        except ImportError:
            print(
                "Warning: Quartz not available. Install with: pip install pyobjc-framework-Quartz"
            )
            self._quartz_available = False

    def press_key(self, key: str, duration: float) -> bool:
        """
        Press and hold a key for the specified duration.

        Args:
            key: The key to press
            duration: How long to hold the key in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self._quartz_available:
            return self._fallback_press_key(key, duration)

        key_lower = key.lower()
        if key_lower not in self._key_codes:
            print(f"Error: Key '{key}' not supported on macOS")
            self._print_supported_keys()
            return False

        try:
            key_code = self._key_codes[key_lower]

            print(f"macOS: Pressing key '{key}' (code: {key_code}) for {duration}s")

            # Create and post key down event
            key_down_event = self._cgEvent(None, key_code, True)
            self._cgPost(self._cgHIDEventTap, key_down_event)

            # Hold the key for the specified duration
            time.sleep(duration)

            # Create and post key up event
            key_up_event = self._cgEvent(None, key_code, False)
            self._cgPost(self._cgHIDEventTap, key_up_event)

            return True

        except Exception as e:
            print(f"macOS keyboard error: {e}")
            return False

    def press_key_combination(self, key_combination: str) -> bool:
        """
        Press a key combination (e.g., 'cmd+shift+f9').

        Args:
            key_combination: The key combination to press

        Returns:
            True if successful, False otherwise
        """
        if not self._quartz_available:
            return self._fallback_press_combination(key_combination)

        # Parse key combination
        if "+" in key_combination:
            parts = [part.strip().lower() for part in key_combination.split("+")]
            main_key = parts[-1]  # Last part is the main key
            modifiers = parts[:-1]  # Everything else are modifiers
        else:
            main_key = key_combination.lower()
            modifiers = []

        # Validate main key
        if main_key not in self._key_codes:
            print(f"Error: Key '{main_key}' not supported on macOS")
            return False

        try:
            key_code = self._key_codes[main_key]

            # Build modifier flags
            flags = 0
            for modifier in modifiers:
                if modifier in self._modifier_masks:
                    flags |= self._modifier_masks[modifier]
                else:
                    print(f"Warning: Unknown modifier '{modifier}' ignored")

            print(
                f"macOS: Pressing key combination '{key_combination}' (code: {key_code}, flags: {flags})"
            )

            # Create key down event with modifiers
            key_down_event = self._cgEvent(None, key_code, True)
            if flags:
                self._cgSetFlags(key_down_event, flags)
            self._cgPost(self._cgHIDEventTap, key_down_event)

            # Brief pause
            time.sleep(0.01)

            # Create key up event
            key_up_event = self._cgEvent(None, key_code, False)
            if flags:
                self._cgSetFlags(key_up_event, flags)
            self._cgPost(self._cgHIDEventTap, key_up_event)

            return True

        except Exception as e:
            print(f"macOS key combination error: {e}")
            return False

    def get_supported_keys(self) -> List[str]:
        """Get a list of supported key names."""
        return list(self._key_codes.keys())

    def is_available(self) -> bool:
        """Check if the keyboard handler is available."""
        return self._quartz_available

    def get_platform_name(self) -> str:
        """Get the platform name."""
        return "macOS"

    def _print_supported_keys(self):
        """Print information about supported keys."""
        print("Supported keys include:")
        print("- Arrow keys: left, right, up, down")
        print("- Letters: a-z")
        print("- Numbers: 0-9")
        print("- Function keys: f1-f12")
        print("- Special: space, enter, tab, shift, cmd, ctrl, alt, escape, delete")

    def _fallback_press_key(self, key: str, duration: float) -> bool:
        """Fallback to generic keyboard library if Quartz is not available."""
        try:
            import keyboard

            keyboard.press(key)
            time.sleep(duration)
            keyboard.release(key)
            return True
        except Exception as e:
            print(f"Fallback keyboard error: {e}")
            return False

    def _fallback_press_combination(self, key_combination: str) -> bool:
        """Fallback key combination press using generic keyboard library."""
        try:
            import keyboard

            keyboard.press_and_release(key_combination)
            return True
        except Exception as e:
            print(f"Fallback key combination error: {e}")
            return False
