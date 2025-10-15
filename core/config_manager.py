"""
Configuration Manager for 360° Game Screenshot Automation

This module provides a clean interface for loading, reading, and writing
configuration data to JSON files with proper error handling and validation.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

class ConfigManager:
    """
    Manages configuration loading, reading, and writing operations.

    Provides a clean interface for handling JSON configuration files
    with proper error handling, default values, and validation.
    """

    def __init__(self, config_file: str = "game_config.json"):
        """
        Initialize the configuration manager.

        Args:
            config_file: Path to the configuration file
        """
        self.config_file = Path(config_file)
        self._config_data: Dict[str, Any] = {}
        self._default_config = self._get_default_config()

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default if it doesn't exist.

        Returns:
            Configuration dictionary
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                print(f"Configuration loaded from: {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading config file: {e}")
                print("Using default configuration.")
                self._config_data = self._default_config.copy()
        else:
            # Create default config file
            self._config_data = self._default_config.copy()
            self.save()
            print(f"Created default config file: {self.config_file}")

        return self._config_data

    def save(self) -> bool:
        """
        Save current configuration to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=4, ensure_ascii=False)
            print(f"Configuration saved to: {self.config_file}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving config file: {e}")
            return False

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a value from the configuration using dot notation.

        Args:
            key_path: Dot-separated path to the configuration value
                     Examples: "games.default.control_type", "defaults.movement.horizontal_steps"
            default: Default value to return if key is not found

        Returns:
            Configuration value or default

        Examples:
            config.get("games.default.control_type")  # Returns "keyboard"
            config.get("games.mygame.movement.horizontal_steps", 36)  # Returns steps or 36
        """
        try:
            current = self._config_data
            for key in key_path.split('.'):
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def has_game(self, game_name: str) -> bool:
        """
        Check if a game configuration exists.

        Args:
            game_name: Name of the game configuration

        Returns:
            True if game configuration exists
        """
        return game_name in self.get("games", {})

    def add_game(self, game_name: str, config: Dict[str, Any]) -> bool:
        """
        Add or update a game configuration.

        Args:
            game_name: Name of the game
            config: Game configuration dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            if "games" not in self._config_data:
                self._config_data["games"] = {}

            self._config_data["games"][game_name] = config
            return True
        except Exception as e:
            print(f"Error adding game '{game_name}': {e}")
            return False

    def get_game_config(self, game_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific game with defaults applied.

        Args:
            game_name: Name of the game

        Returns:
            Game configuration dictionary with defaults merged, or None if not found
        """
        game_config = self.get(f"games.{game_name}")
        if not game_config:
            return None

        # Merge with defaults to ensure all values are present
        return self._merge_with_defaults(game_config)

    def _merge_with_defaults(self, game_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge game configuration with defaults to ensure all required values are present.

        Args:
            game_config: Game configuration dictionary

        Returns:
            Merged configuration with defaults applied
        """
        import copy

        # Start with defaults
        defaults = self.get_defaults()
        merged_config = copy.deepcopy(game_config)

        # Merge movement settings
        if "movement" not in merged_config:
            merged_config["movement"] = {}
        for key, value in defaults.get("movement", {}).items():
            if key not in merged_config["movement"]:
                merged_config["movement"][key] = value

        # Merge screenshot settings
        if "screenshot" not in merged_config:
            merged_config["screenshot"] = {}
        for key, value in defaults.get("screenshot", {}).items():
            if key not in merged_config["screenshot"]:
                merged_config["screenshot"][key] = value

        # Merge control settings
        if "controls" not in merged_config:
            merged_config["controls"] = {}

        control_type = merged_config.get("control_type", "keyboard")
        if control_type in defaults.get("controls", {}):
            if control_type not in merged_config["controls"]:
                merged_config["controls"][control_type] = {}
            for key, value in defaults["controls"][control_type].items():
                if key not in merged_config["controls"][control_type]:
                    merged_config["controls"][control_type][key] = value

        return merged_config

    def list_games(self) -> list:
        """
        Get list of configured games.

        Returns:
            List of game names
        """
        games = self.get("games", {})
        return list(games.keys())

    def get_defaults(self) -> Dict[str, Any]:
        """
        Get default configuration values.

        Returns:
            Default configuration dictionary
        """
        return self.get("defaults", {})

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration structure.

        Returns:
            Default configuration dictionary
        """
        from .constants import (
            DEFAULT_HORIZONTAL_STEPS, DEFAULT_VERTICAL_STEPS,
            DEFAULT_HORIZONTAL_MOVEMENT_DURATION, DEFAULT_VERTICAL_MOVEMENT_DURATION,
            DEFAULT_PAUSE_BETWEEN_MOVES, DEFAULT_SCREENSHOT_KEY,
            DEFAULT_SCREENSHOT_DELAY, DEFAULT_SCREENSHOT_PAUSE,
            DEFAULT_GAMEPAD_STICK_MOVEMENT, DEFAULT_MOUSE_SENSITIVITY,
            DEFAULT_MOUSE_CAPTURE, DEFAULT_KEY_LEFT, DEFAULT_KEY_RIGHT,
            DEFAULT_KEY_UP, DEFAULT_KEY_DOWN, DEFAULT_CONFIG_VERSION
        )

        return {
            "_comment": "360° Game Screenshot Automation Configuration",
            "_version": DEFAULT_CONFIG_VERSION,
            "defaults": {
                "movement": {
                    "horizontal_steps": DEFAULT_HORIZONTAL_STEPS,
                    "vertical_steps": DEFAULT_VERTICAL_STEPS,
                    "horizontal_movement_duration": DEFAULT_HORIZONTAL_MOVEMENT_DURATION,
                    "vertical_movement_duration": DEFAULT_VERTICAL_MOVEMENT_DURATION,
                    "pause_between_moves": DEFAULT_PAUSE_BETWEEN_MOVES
                },
                "screenshot": {
                    "key": DEFAULT_SCREENSHOT_KEY,
                    "delay": DEFAULT_SCREENSHOT_DELAY,
                    "pause": DEFAULT_SCREENSHOT_PAUSE
                },
                "controls": {
                    "keyboard": {
                        "left": DEFAULT_KEY_LEFT,
                        "right": DEFAULT_KEY_RIGHT,
                        "up": DEFAULT_KEY_UP,
                        "down": DEFAULT_KEY_DOWN
                    },
                    "gamepad": {
                        "stick_movement_amount": DEFAULT_GAMEPAD_STICK_MOVEMENT
                    },
                    "mouse": {
                        "sensitivity": DEFAULT_MOUSE_SENSITIVITY,
                        "capture_mouse": DEFAULT_MOUSE_CAPTURE
                    }
                }
            },
            "games": {
                "default": {
                    "description": "Default configuration template",
                    "control_type": "keyboard",
                    "movement": {
                        "horizontal_steps": DEFAULT_HORIZONTAL_STEPS,
                        "vertical_steps": DEFAULT_VERTICAL_STEPS,
                        "horizontal_movement_duration": DEFAULT_HORIZONTAL_MOVEMENT_DURATION,
                        "vertical_movement_duration": DEFAULT_VERTICAL_MOVEMENT_DURATION,
                        "pause_between_moves": DEFAULT_PAUSE_BETWEEN_MOVES
                    },
                    "screenshot": {
                        "key": DEFAULT_SCREENSHOT_KEY,
                        "delay": DEFAULT_SCREENSHOT_DELAY,
                        "pause": DEFAULT_SCREENSHOT_PAUSE
                    },
                    "controls": {
                        "keyboard": {
                            "left": DEFAULT_KEY_LEFT,
                            "right": DEFAULT_KEY_RIGHT,
                            "up": DEFAULT_KEY_UP,
                            "down": DEFAULT_KEY_DOWN
                        }
                    }
                }
            }
        }

    def __repr__(self) -> str:
        """String representation of the config manager."""
        games_count = len(self.list_games())
        return f"ConfigManager(file='{self.config_file}', games={games_count})"
