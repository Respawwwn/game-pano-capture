"""
Cross-platform game control module for automation.

This module provides platform-specific implementations for various input methods
including keyboard, mouse, and gamepad controls with a unified interface.
"""

from .gamepad import GamepadFactory
from .keyboard import KeyboardFactory
from .mouse import MouseFactory

__all__ = ["KeyboardFactory", "MouseFactory", "GamepadFactory"]
