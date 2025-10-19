"""Shared fixtures for CLI tester tests."""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_factories():
    """Create mock factories for all tests."""
    # Mock keyboard factory
    mock_keyboard_factory = Mock()
    mock_keyboard_handler = Mock()
    mock_keyboard_handler.press_key.return_value = True
    mock_keyboard_handler.press_key_combination.return_value = True
    mock_keyboard_handler.is_available.return_value = True
    mock_keyboard_handler.get_platform_name.return_value = "Mock"
    mock_keyboard_factory.create_handler.return_value = mock_keyboard_handler

    # Mock mouse factory
    mock_mouse_factory = Mock()
    mock_mouse_handler = Mock()
    mock_mouse_handler.move_relative.return_value = True
    mock_mouse_handler.is_available.return_value = True
    mock_mouse_handler.get_platform_name.return_value = "Mock"
    mock_mouse_factory.create_handler.return_value = mock_mouse_handler

    # Mock gamepad factory
    mock_gamepad_factory = Mock()
    mock_gamepad_handler = Mock()
    mock_gamepad_handler.move_stick.return_value = True
    mock_gamepad_handler.is_available.return_value = True
    mock_gamepad_handler.initialize.return_value = True
    mock_gamepad_handler.get_platform_name.return_value = "Mock"
    mock_gamepad_factory.create_handler.return_value = mock_gamepad_handler

    return {
        "keyboard": mock_keyboard_factory,
        "mouse": mock_mouse_factory,
        "gamepad": mock_gamepad_factory,
    }


@pytest.fixture(autouse=True)
def setup_path():
    """Automatically setup sys.path for all tests."""
    test_root = Path(__file__).parent.parent.parent.parent.parent
    sys.path.insert(0, str(test_root))
    yield
    # Clean up path after test
    if str(test_root) in sys.path:
        sys.path.remove(str(test_root))
