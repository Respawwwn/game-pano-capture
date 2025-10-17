"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_config_data():
    """Sample configuration data for testing."""
    return {
        "horizontal_steps": 12,
        "vertical_steps": 3,
        "screenshot_key": "f12",
        "mouse_sensitivity": 1.0,
        "gamepad_stick_movement": 0.8,
    }
