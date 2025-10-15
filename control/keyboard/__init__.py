"""
Cross-platform keyboard handling module for game automation.

This module provides platform-specific keyboard implementations with a unified interface.
"""

from .interface import IKeyboardHandler
from .factory import KeyboardFactory

__all__ = ['IKeyboardHandler', 'KeyboardFactory']