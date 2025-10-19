"""
Interface definition for keyboard handlers.

This module defines the contract that all platform-specific keyboard implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import List


class IKeyboardHandler(ABC):
    """
    Interface for platform-specific keyboard implementations.

    All keyboard handlers must implement this interface to ensure
    consistent behavior across different platforms.
    """

    @abstractmethod
    def press_key(self, key: str, duration: float) -> bool:
        """
        Press and hold a key for the specified duration.

        Args:
            key: The key to press (e.g., 'k', 'left', 'f9')
            duration: How long to hold the key in seconds

        Returns:
            True if successful, False otherwise

        Raises:
            NotImplementedError: If the method is not implemented
        """

    @abstractmethod
    def press_key_combination(self, key_combination: str) -> bool:
        """
        Press a key combination (e.g., 'cmd+shift+f9').

        Args:
            key_combination: The key combination to press.
                           Modifiers and main key should be separated by '+'
                           Examples: 'ctrl+c', 'cmd+shift+f9', 'alt+tab'

        Returns:
            True if successful, False otherwise

        Raises:
            NotImplementedError: If the method is not implemented
        """

    @abstractmethod
    def get_supported_keys(self) -> List[str]:
        """
        Get a list of supported key names for this platform.

        Returns:
            List of supported key names as strings

        Raises:
            NotImplementedError: If the method is not implemented
        """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the keyboard handler is available and properly initialized.

        Returns:
            True if the handler is available and can be used, False otherwise

        Raises:
            NotImplementedError: If the method is not implemented
        """

    @abstractmethod
    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.

        Returns:
            Platform name as a string (e.g., 'macOS', 'Windows', 'Linux')

        Raises:
            NotImplementedError: If the method is not implemented
        """
