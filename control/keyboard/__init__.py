"""
Cross-platform keyboard handling module for game automation.

This module provides platform-specific keyboard implementations with a unified interface.
"""

from .factory import KeyboardFactory
from .interface import IKeyboardHandler

__all__ = ["IKeyboardHandler", "KeyboardFactory"]
