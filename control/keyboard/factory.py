"""
Factory for creating platform-specific keyboard handlers.

This module provides a factory class that automatically detects the current platform
and returns the appropriate keyboard handler implementation.
"""

import platform
from typing import Optional

from .interface import IKeyboardHandler


class KeyboardFactory:
    """
    Factory class for creating platform-specific keyboard handlers.

    This factory automatically detects the current platform and returns
    the most appropriate keyboard handler implementation.
    """

    _cached_handler: Optional[IKeyboardHandler] = None
    _platform_handlers = {"Darwin": "macos", "Windows": "windows", "Linux": "generic"}

    @classmethod
    def create_handler(cls, force_platform: Optional[str] = None) -> IKeyboardHandler:
        """
        Create and return a keyboard handler for the current platform.

        Args:
            force_platform: Optional platform name to force a specific handler.
                           Valid values: 'macos', 'windows', 'generic'
                           If None, auto-detects the current platform.

        Returns:
            Platform-specific keyboard handler instance

        Raises:
            ImportError: If the platform-specific handler cannot be imported
            RuntimeError: If an unsupported platform is detected
        """
        # Return cached handler if available and no specific platform is forced
        if cls._cached_handler is not None and force_platform is None:
            return cls._cached_handler

        # Determine which handler to use
        if force_platform:
            handler_module = force_platform.lower()
        else:
            system = platform.system()
            handler_module = cls._platform_handlers.get(system, "generic")

        # Import and create the appropriate handler
        try:
            if handler_module == "macos":
                from .macos import MacOSKeyboardHandler

                handler = MacOSKeyboardHandler()
            elif handler_module == "windows":
                from .windows import WindowsKeyboardHandler

                handler = WindowsKeyboardHandler()
            elif handler_module == "generic":
                from .generic import GenericKeyboardHandler

                handler = GenericKeyboardHandler()
            else:
                raise RuntimeError(f"Unsupported keyboard handler: {handler_module}")

        except ImportError as e:
            raise ImportError(
                f"Failed to import keyboard handler '{handler_module}': {e}"
            ) from e

        # Cache the handler if no specific platform was forced
        if force_platform is None:
            cls._cached_handler = handler

        return handler

    @classmethod
    def get_available_platforms(cls) -> list:
        """
        Get a list of available platform handlers.

        Returns:
            List of available platform handler names
        """
        import importlib.util

        available = []

        # Check macOS handler
        if importlib.util.find_spec(".macos", package=__package__):
            available.append("macos")

        # Check Windows handler
        if importlib.util.find_spec(".windows", package=__package__):
            available.append("windows")

        # Check generic handler
        if importlib.util.find_spec(".generic", package=__package__):
            available.append("generic")

        return available

    @classmethod
    def clear_cache(cls):
        """Clear the cached handler instance."""
        cls._cached_handler = None

    @classmethod
    def get_current_platform(cls) -> str:
        """
        Get the current platform name.

        Returns:
            Current platform name (e.g., 'Darwin', 'Windows', 'Linux')
        """
        return platform.system()

    @classmethod
    def get_recommended_handler(cls) -> str:
        """
        Get the recommended handler name for the current platform.

        Returns:
            Recommended handler name for the current platform
        """
        system = platform.system()
        return cls._platform_handlers.get(system, "generic")
