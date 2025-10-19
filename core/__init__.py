"""
Core modules for 360° Game Screenshot Automation.

This package contains the core functionality including configuration management,
utilities, and common interfaces used throughout the application.
"""

from .config_manager import ConfigManager
from .constants import ConfigDefaults

__all__ = ["ConfigManager", "ConfigDefaults"]
