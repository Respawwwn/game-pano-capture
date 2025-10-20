"""Tests for ConfigManager class."""

import json
from pathlib import Path

import pytest

from core.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""

    @pytest.mark.unit
    def test_init_default_config_file(self):
        """Test initialization with default config file name."""
        config_manager = ConfigManager()
        assert config_manager.config_file == Path("game_config.json")

    @pytest.mark.unit
    def test_init_custom_config_file(self):
        """Test initialization with custom config file name."""
        config_manager = ConfigManager("custom_config.json")
        assert config_manager.config_file == Path("custom_config.json")

    @pytest.mark.unit
    def test_load_nonexistent_file_creates_default(self, temp_config_dir):
        """Test loading config when file doesn't exist creates default config."""
        config_file = temp_config_dir / "test_config.json"
        config_manager = ConfigManager(str(config_file))

        config = config_manager.load()

        # Should create default config with nested structure
        assert isinstance(config, dict)
        assert "_comment" in config
        assert "defaults" in config
        assert "games" in config
        assert config["defaults"]["movement"]["horizontal_steps"] == 13

        # Config file should be created
        assert config_file.exists()

    @pytest.mark.unit
    def test_load_existing_valid_file(self, temp_config_dir, sample_config_data):
        """Test loading existing valid config file."""
        config_file = temp_config_dir / "test_config.json"

        # Create a test config file
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(sample_config_data, f)

        config_manager = ConfigManager(str(config_file))
        config = config_manager.load()

        assert config == sample_config_data

    @pytest.mark.unit
    def test_load_invalid_json_uses_default(self, temp_config_dir, capsys):
        """Test loading invalid JSON file falls back to default."""
        config_file = temp_config_dir / "invalid_config.json"

        # Create invalid JSON
        with open(config_file, "w", encoding="utf-8") as f:
            f.write("invalid json content")

        config_manager = ConfigManager(str(config_file))
        config = config_manager.load()

        # Should use default config with nested structure
        assert isinstance(config, dict)
        assert "defaults" in config
        assert config["defaults"]["movement"]["horizontal_steps"] == 13

        # Should print error message
        captured = capsys.readouterr()
        assert "Error reading config file" in captured.out

    @pytest.mark.unit
    def test_get_nested_value_with_dot_notation(self):
        """Test getting nested value using dot notation."""
        config_manager = ConfigManager()
        config_manager._config_data = {
            "defaults": {"movement": {"horizontal_steps": 24}}
        }

        value = config_manager.get("defaults.movement.horizontal_steps")
        assert value == 24

    @pytest.mark.unit
    def test_get_value_nonexistent_key_with_default(self):
        """Test getting value for non-existent key returns default."""
        config_manager = ConfigManager()
        config_manager._config_data = {"existing_key": "value"}

        value = config_manager.get("nonexistent_key", "default_value")
        assert value == "default_value"

    @pytest.mark.unit
    def test_get_value_nonexistent_key_no_default(self):
        """Test getting value for non-existent key without default returns None."""
        config_manager = ConfigManager()
        config_manager._config_data = {"existing_key": "value"}

        value = config_manager.get("nonexistent_key")
        assert value is None

    @pytest.mark.unit
    def test_save_config(self, temp_config_dir):
        """Test saving configuration to file."""
        config_file = temp_config_dir / "save_test.json"
        config_manager = ConfigManager(str(config_file))
        config_manager._config_data = {"test_key": "test_value"}

        result = config_manager.save()

        assert result is True
        assert config_file.exists()

        # Verify content
        with open(config_file, encoding="utf-8") as f:
            saved_data = json.load(f)
        assert saved_data == {"test_key": "test_value"}

    @pytest.mark.unit
    def test_has_game_existing(self):
        """Test checking for existing game."""
        config_manager = ConfigManager()
        config_manager._config_data = {
            "games": {"test_game": {"control_type": "keyboard"}}
        }

        assert config_manager.has_game("test_game") is True

    @pytest.mark.unit
    def test_has_game_nonexistent(self):
        """Test checking for non-existent game."""
        config_manager = ConfigManager()
        config_manager._config_data = {"games": {}}

        assert config_manager.has_game("nonexistent_game") is False

    @pytest.mark.unit
    def test_add_game(self):
        """Test adding a new game configuration."""
        config_manager = ConfigManager()
        config_manager._config_data = {}

        game_config = {"control_type": "keyboard", "description": "Test game"}
        result = config_manager.add_game("test_game", game_config)

        assert result is True
        assert config_manager._config_data["games"]["test_game"] == game_config

    @pytest.mark.unit
    def test_get_game_config(self):
        """Test getting game configuration with defaults merged."""
        config_manager = ConfigManager()
        config_manager.load()  # Load default config

        # Add a minimal game config
        game_config = {"control_type": "keyboard"}
        config_manager.add_game("test_game", game_config)

        result = config_manager.get_game_config("test_game")

        assert result is not None
        assert "movement" in result  # Should be merged from defaults
        assert "screenshot" in result  # Should be merged from defaults

    @pytest.mark.unit
    def test_list_games(self):
        """Test listing all configured games."""
        config_manager = ConfigManager()
        config_manager._config_data = {"games": {"game1": {}, "game2": {}, "game3": {}}}

        games = config_manager.list_games()
        assert set(games) == {"game1", "game2", "game3"}

    @pytest.mark.unit
    def test_get_defaults(self):
        """Test getting default configuration values."""
        config_manager = ConfigManager()
        config_manager.load()  # Load default config

        defaults = config_manager.get_defaults()

        assert isinstance(defaults, dict)
        assert "movement" in defaults
        assert "screenshot" in defaults
        assert "controls" in defaults
