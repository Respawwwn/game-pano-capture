"""
Gamepad control module for cross-platform gamepad handling.

This module provides platform-specific gamepad implementations for game control.
"""

from .factory import GamepadFactory

__all__ = ['GamepadFactory']