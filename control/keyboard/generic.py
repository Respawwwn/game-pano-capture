"""
Generic keyboard implementation for Linux and other Unix-like systems.
"""

import time
from typing import List

from .interface import IKeyboardHandler


class GenericKeyboardHandler(IKeyboardHandler):
    """Generic keyboard handler using the keyboard library for Linux and other systems."""
    
    def __init__(self):
        self._keyboard_available = False
        self._keyboard = None
        
        # Try to import keyboard library
        try:
            import keyboard
            self._keyboard = keyboard
            self._keyboard_available = True
            print("Generic: keyboard library initialized")
        except ImportError:
            print("Warning: keyboard library not available. Install with: pip install keyboard")
            print("Note: On Linux, you may need to run with sudo for keyboard access")
    
    def press_key(self, key: str, duration: float) -> bool:
        """
        Press and hold a key for the specified duration.
        
        Args:
            key: The key to press
            duration: How long to hold the key in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self._keyboard_available:
            print("Error: No keyboard library available")
            return False
        
        try:
            print(f"Generic: Pressing key '{key}' for {duration}s")
            
            self._keyboard.press(key)
            time.sleep(duration)
            self._keyboard.release(key)
            
            return True
            
        except ValueError as e:
            print(f"Error: Key '{key}' is not supported by the keyboard library")
            print("Try using standard key names like 'left', 'right', 'up', 'down'")
            print("Note: On Linux, you may need to run with sudo for keyboard access")
            print(f"Original error: {e}")
            return False
        except Exception as e:
            print(f"Generic keyboard error: {e}")
            print("Note: On Linux, you may need to run with sudo for keyboard access")
            return False
    
    def press_key_combination(self, key_combination: str) -> bool:
        """
        Press a key combination (e.g., 'ctrl+shift+f9').
        
        Args:
            key_combination: The key combination to press
            
        Returns:
            True if successful, False otherwise
        """
        if not self._keyboard_available:
            print("Error: No keyboard library available")
            return False
        
        try:
            print(f"Generic: Pressing key combination '{key_combination}'")
            
            self._keyboard.press_and_release(key_combination)
            return True
            
        except ValueError as e:
            print(f"Error: Key combination '{key_combination}' is not supported")
            print("Try using standard key names or check the keyboard library documentation")
            print("Note: On Linux, you may need to run with sudo for keyboard access")
            print(f"Original error: {e}")
            return False
        except Exception as e:
            print(f"Generic key combination error: {e}")
            print("Note: On Linux, you may need to run with sudo for keyboard access")
            return False
    
    def get_supported_keys(self) -> List[str]:
        """
        Get a list of supported key names.
        
        Note: The keyboard library supports many keys, but the exact list
        depends on the system configuration and permissions.
        """
        # Common keys that should work on most Linux systems
        return [
            'left', 'right', 'up', 'down',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
            'space', 'enter', 'tab', 'shift', 'ctrl', 'alt', 'escape', 'delete'
        ]
    
    def is_available(self) -> bool:
        """Check if the keyboard handler is available."""
        return self._keyboard_available
    
    def get_platform_name(self) -> str:
        """Get the platform name."""
        return "Linux/Generic"