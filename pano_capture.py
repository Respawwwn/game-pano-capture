#!/usr/bin/env python3
"""
360° Game Screenshot Automation Script
Automates the capture of panoramic screenshots from video games for photosphere creation.
Uses configurable keybinds to trigger external screenshot tools.
"""

import time
import os
import json
import platform
from datetime import datetime
from pathlib import Path
import argparse
import pygame
from control import KeyboardFactory
from core import ConfigManager, ConfigDefaults
from core.constants import (
    DEFAULT_HORIZONTAL_STEPS, DEFAULT_VERTICAL_STEPS,
    DEFAULT_HORIZONTAL_MOVEMENT_DURATION, DEFAULT_VERTICAL_MOVEMENT_DURATION,
    DEFAULT_PAUSE_BETWEEN_MOVES, DEFAULT_SCREENSHOT_KEY,
    DEFAULT_SCREENSHOT_DELAY, DEFAULT_SCREENSHOT_PAUSE,
    DEFAULT_GAMEPAD_STICK_MOVEMENT, DEFAULT_MOUSE_SENSITIVITY,
    CAPTURE_COUNTDOWN_SECONDS
)

class GamePanoCapture:
    def __init__(self, config_file="game_config.json"):
        # Initialize configuration manager
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.load()

        self.screenshot_count = 0
        self.output_dir = None
        self.gamepad = None
        self.gamepad_initialized = False
        self.virtual_gamepad = None
        self.pygame_initialized = False
        self.mouse_initialized = False

        # Initialize platform-specific keyboard handler
        self.keyboard_handler = KeyboardFactory.create_handler()

    def setup_output_directory(self, game_name="capture"):
        """Create output directory for session info"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"captures/panorama_capture_{game_name}_{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Session info will be saved to: {self.output_dir}")

    def init_gamepad(self, game_config):
        """Initialize virtual gamepad if needed"""
        if game_config["control_type"] != "gamepad":
            return True

        if self.gamepad_initialized:
            return True

        # Check if we're on Windows
        if platform.system() != "Windows":
            print("Error: Virtual gamepad support (vgamepad) is only available on Windows")
            print("On non-Windows platforms, please use keyboard or mouse control types")
            return False

        try:
            # Import vgamepad only on Windows
            import vgamepad as vg
            # Create virtual Xbox 360 gamepad
            self.virtual_gamepad = vg.VX360Gamepad()
            print("Virtual Xbox 360 gamepad created successfully")
            self.gamepad_initialized = True
            return True

        except ImportError:
            print("Error: vgamepad not available - gamepad support requires vgamepad package")
            print("Install vgamepad with: pip install vgamepad")
            print("Note: vgamepad only works on Windows")
            return False
        except Exception as e:
            print(f"Error initializing virtual gamepad: {e}")
            return False

    def init_mouse(self, game_config):
        """Initialize mouse control if needed"""
        if game_config["control_type"] != "mouse":
            return True

        if self.mouse_initialized:
            return True

        try:
            print("Initializing mouse control...")
            print("IMPORTANT: Make sure the game window is in focus when testing!")
            print("The mouse will send relative movements to the active window.")

            # Initialize pygame for mouse events (but don't capture)
            if not self.pygame_initialized:
                pygame.init()
                self.pygame_initialized = True
                print("Pygame initialized for mouse control")

            self.mouse_initialized = True
            return True

        except Exception as e:
            print(f"Error initializing mouse control: {e}")
            return False

    def take_screenshot(self, screenshot_number, game_config):
        """Trigger screenshot using configured keybind"""
        try:
            screenshot_config = game_config["screenshot"]
            screenshot_key = screenshot_config["key"]
            print(f"Taking screenshot {screenshot_number:04d} (pressing {screenshot_key})...")

            # Use platform-specific keyboard handler.
            success = self.keyboard_handler.press_key_combination(screenshot_key)

            if success:
                # Wait for screenshot to be processed by external tool
                screenshot_pause = screenshot_config["pause"]
                time.sleep(screenshot_pause)
                return True
            else:
                return False

        except Exception as e:
            print(f"Error triggering screenshot: {e}")
            return False

    def move_camera(self, direction, game_config):
        """Move camera in specified direction"""
        # Get movement settings from new structure
        movement_config = game_config.get("movement", {})

        # Determine movement duration based on direction
        if direction in ["left", "right"]:
            movement_duration = movement_config["horizontal_movement_duration"]
        else:  # up, down
            movement_duration = movement_config["vertical_movement_duration"]

        if game_config["control_type"] == "keyboard":
            controls_config = game_config.get("controls", {}).get("keyboard", {})
            key = controls_config.get(direction, direction)

            # Use platform-specific keyboard handler
            success = self.keyboard_handler.press_key(key, movement_duration)
            if not success:
                return
        elif game_config["control_type"] == "gamepad":
            if not self.init_gamepad(game_config):
                print("Error: Could not initialize gamepad")
                return

            # Get movement amount from config
            controls_config = game_config.get("controls", {}).get("gamepad", {})
            from core.constants import DEFAULT_GAMEPAD_STICK_MOVEMENT
            stick_amount = controls_config.get("stick_movement_amount", DEFAULT_GAMEPAD_STICK_MOVEMENT)

            # Map directions to right stick movements
            if direction == "right":
                x_axis = stick_amount
                y_axis = 0.0
            elif direction == "left":
                x_axis = -stick_amount
                y_axis = 0.0
            elif direction == "up":
                x_axis = 0.0
                y_axis = stick_amount  # Positive Y is up on most game right sticks.
            elif direction == "down":
                x_axis = 0.0
                y_axis = -stick_amount   # Negative Y is down on most game right sticks.
            else:
                print(f"Unknown direction: {direction}")
                return

            # Simulate right stick movement using vgamepad
            try:
                print(f"Moving virtual gamepad right stick: {direction} (x={x_axis:.1f}, y={y_axis:.1f})")

                if self.virtual_gamepad:
                    # Set right stick position using vgamepad
                    self.virtual_gamepad.right_joystick_float(x_value_float=x_axis, y_value_float=y_axis)
                    self.virtual_gamepad.update()

                    # Hold the movement for the specified duration
                    time.sleep(movement_duration)

                    # Release the stick (return to center)
                    self.virtual_gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                    self.virtual_gamepad.update()
                else:
                    print("Error: Virtual gamepad not initialized")

            except Exception as e:
                print(f"Error moving virtual gamepad stick: {e}")

        elif game_config["control_type"] == "mouse":
            if not self.init_mouse(game_config):
                print("Error: Could not initialize mouse control")
                return

            # Get mouse movement amount from config
            controls_config = game_config.get("controls", {}).get("mouse", {})
            sensitivity = controls_config.get("sensitivity", DEFAULT_MOUSE_SENSITIVITY)

            # Map directions to mouse movements
            if direction == "right":
                mouse_x = sensitivity
                mouse_y = 0
            elif direction == "left":
                mouse_x = -sensitivity
                mouse_y = 0
            elif direction == "up":
                mouse_x = 0
                mouse_y = -sensitivity  # Negative Y is up for mouse
            elif direction == "down":
                mouse_x = 0
                mouse_y = sensitivity   # Positive Y is down for mouse
            else:
                print(f"Unknown direction: {direction}")
                return

            # Simulate relative mouse movement
            try:
                print(f"Moving mouse: {direction} (relative x={mouse_x}, y={mouse_y})")

                # Use platform-specific relative mouse movement
                if platform.system() == "Windows":
                    # Use win32api for Windows relative movement
                    try:
                        import win32api, win32con
                        # Send relative mouse movement using SendInput-like approach
                        # This simulates actual mouse movement that games can detect

                        # Method 1: Try relative mouse_event (deprecated but works)
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, mouse_x, mouse_y, 0, 0)
                        print(f"Windows: Sent relative mouse movement (dx={mouse_x}, dy={mouse_y})")

                    except ImportError:
                        print("win32api not available - mouse movement may not work in games")
                        print("Install pywin32 with: pip install pywin32")
                        # Fallback to absolute positioning (won't work in most games)
                        current_pos = pygame.mouse.get_pos()
                        new_x = current_pos[0] + mouse_x
                        new_y = current_pos[1] + mouse_y
                        pygame.mouse.set_pos((new_x, new_y))
                        print(f"Pygame fallback: Moved mouse from {current_pos} to ({new_x}, {new_y})")

                    except Exception as e:
                        print(f"Windows mouse error: {e}")
                        print("Trying alternative method...")
                        # Try alternative win32 method
                        try:
                            import win32gui
                            # Get current cursor position and move relatively
                            current_x, current_y = win32api.GetCursorPos()
                            new_x = current_x + mouse_x
                            new_y = current_y + mouse_y
                            win32api.SetCursorPos((new_x, new_y))
                            print(f"Windows absolute: Moved from ({current_x}, {current_y}) to ({new_x}, {new_y})")
                        except:
                            print("All Windows mouse methods failed")
                else:
                    # For non-Windows platforms, use pygame
                    print("Non-Windows platform: Using pygame mouse control")
                    current_pos = pygame.mouse.get_pos()
                    new_x = current_pos[0] + mouse_x
                    new_y = current_pos[1] + mouse_y
                    pygame.mouse.set_pos((new_x, new_y))
                    print(f"Pygame: Moved mouse from {current_pos} to ({new_x}, {new_y})")

                # Hold the movement for the specified duration
                time.sleep(movement_duration)

                # Process any pygame events
                if self.pygame_initialized:
                    pygame.event.pump()

            except Exception as e:
                print(f"Error moving mouse: {e}")
                print(f"Platform: {platform.system()}")
                print("Mouse control troubleshooting:")
                print("1. Make sure the game window is in focus")
                print("2. On Windows, install pywin32: pip install pywin32")
                print("3. Some games may not respond to programmatic mouse input")
                print("4. Try increasing mouse sensitivity in the config")

        movement_config = game_config["movement"]
        time.sleep(movement_config["pause_between_moves"])

    def capture_panorama(self, game_name="default"):
        """Main capture routine"""
        if not self.config_manager.has_game(game_name):
            print(f"Game '{game_name}' not found in config. Using default.")
            game_name = "default"

        game_config = self.config_manager.get_game_config(game_name)

        # Initialize control system if needed
        if game_config["control_type"] == "gamepad":
            if not self.init_gamepad(game_config):
                print("Failed to initialize gamepad. Aborting capture.")
                return
        elif game_config["control_type"] == "mouse":
            if not self.init_mouse(game_config):
                print("Failed to initialize mouse control. Aborting capture.")
                return

        # Get configuration sections
        movement_config = game_config["movement"]
        screenshot_config = game_config["screenshot"]

        print(f"\n=== 360° Panorama Capture Started ===")
        print(f"Game: {game_name}")
        print(f"Horizontal steps: {movement_config.get('horizontal_steps', DEFAULT_HORIZONTAL_STEPS)}")
        print(f"Vertical steps: {movement_config.get('vertical_steps', DEFAULT_VERTICAL_STEPS)}")
        print(f"Control type: {game_config['control_type']}")
        print(f"Screenshot key: {screenshot_config['key']}")

        print(f"\nStarting capture in {CAPTURE_COUNTDOWN_SECONDS} seconds...")
        print("Make sure the game is in focus and camera is at zenith position (straight up)!")
        print("Make sure your screenshot tool is ready!")
        print(f"Screenshot key: {screenshot_config['key']}")
        print("Press Ctrl+C to abort at any time.")

        for i in range(CAPTURE_COUNTDOWN_SECONDS, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        self.setup_output_directory(game_name)
        self.screenshot_count = 0

        try:
            # Start from zenith and work downwards
            horizontal_steps = movement_config.get("horizontal_steps", DEFAULT_HORIZONTAL_STEPS)
            vertical_steps = movement_config.get("vertical_steps", DEFAULT_VERTICAL_STEPS)

            for vertical_step in range(vertical_steps + 1):
                print(f"\nVertical level {vertical_step + 1}/{vertical_steps + 1}")

                # Take screenshots for complete horizontal rotation
                for horizontal_step in range(horizontal_steps):
                    # Take screenshot using configured keybind
                    screenshot_delay = screenshot_config.get("delay", DEFAULT_SCREENSHOT_DELAY)
                    time.sleep(screenshot_delay)
                    if self.take_screenshot(self.screenshot_count + 1, game_config):
                        self.screenshot_count += 1

                    # Move right (except on last horizontal step)
                    if horizontal_step < horizontal_steps - 1:
                        self.move_camera("right", game_config)

                # Move down for next vertical level (except on last vertical step)
                if vertical_step < vertical_steps:
                    self.move_camera("down", game_config)

            print(f"\n=== Capture Complete ===")
            print(f"Total screenshots taken: {self.screenshot_count}")
            print(f"Check your screenshot tool's output folder for the images")
            print(f"Session info saved to: {self.output_dir}")

            # Save session info
            session_info = {
                "game": game_name,
                "timestamp": datetime.now().isoformat(),
                "screenshots_taken": self.screenshot_count,
                "config_used": game_config,
                "expected_screenshots": horizontal_steps * (vertical_steps + 1),
                "capture_pattern": "spherical_zenith_to_nadir"
            }
            with open(self.output_dir / "session_info.json", 'w') as f:
                json.dump(session_info, f, indent=4)

        except KeyboardInterrupt:
            print(f"\n=== Capture Interrupted ===")
            print(f"Screenshots taken: {self.screenshot_count}")
            print(f"Partial capture info saved to: {self.output_dir}")

            # Save partial session info
            session_info = {
                "game": game_name,
                "timestamp": datetime.now().isoformat(),
                "screenshots_taken": self.screenshot_count,
                "config_used": game_config,
                "status": "interrupted",
                "expected_screenshots": horizontal_steps * (vertical_steps + 1)
            }
            with open(self.output_dir / "session_info.json", 'w') as f:
                json.dump(session_info, f, indent=4)

    def create_game_config(self, game_name):
        """Interactive setup for a new game configuration"""
        print(f"\n=== Setting up configuration for '{game_name}' ===")

        # Control type
        control_type = input("Control type (keyboard/gamepad/mouse) [keyboard]: ").lower()
        if control_type not in ["keyboard", "gamepad", "mouse"]:
            control_type = "keyboard"

        # Screenshot configuration
        print("\n--- Screenshot Settings ---")
        screenshot_key = input(f"Screenshot keybind (e.g., 'f9', 'ctrl+shift+s', 'alt+4') [{DEFAULT_SCREENSHOT_KEY}]: ") or DEFAULT_SCREENSHOT_KEY
        screenshot_delay = float(input(f"Delay before screenshot in seconds [{DEFAULT_SCREENSHOT_DELAY}]: ") or str(DEFAULT_SCREENSHOT_DELAY))
        screenshot_pause = float(input(f"Pause after screenshot in seconds [{DEFAULT_SCREENSHOT_PAUSE}]: ") or str(DEFAULT_SCREENSHOT_PAUSE))

        # Movement configuration
        print("\n--- Movement Settings ---")
        horizontal_steps = int(input(f"Horizontal steps for complete rotation [{DEFAULT_HORIZONTAL_STEPS}]: ") or str(DEFAULT_HORIZONTAL_STEPS))
        vertical_steps = int(input(f"Vertical steps from zenith to nadir [{DEFAULT_VERTICAL_STEPS}]: ") or str(DEFAULT_VERTICAL_STEPS))
        horizontal_movement_duration = float(input(f"Horizontal movement duration in seconds [{DEFAULT_HORIZONTAL_MOVEMENT_DURATION}]: ") or str(DEFAULT_HORIZONTAL_MOVEMENT_DURATION))
        vertical_movement_duration = float(input(f"Vertical movement duration in seconds [{DEFAULT_VERTICAL_MOVEMENT_DURATION}]: ") or str(DEFAULT_VERTICAL_MOVEMENT_DURATION))
        pause_between_moves = float(input(f"Pause between moves in seconds [{DEFAULT_PAUSE_BETWEEN_MOVES}]: ") or str(DEFAULT_PAUSE_BETWEEN_MOVES))

        # Create new configuration structure
        config = {
            "description": f"Configuration for {game_name}",
            "control_type": control_type,
            "movement": {
                "horizontal_steps": horizontal_steps,
                "vertical_steps": vertical_steps,
                "horizontal_movement_duration": horizontal_movement_duration,
                "vertical_movement_duration": vertical_movement_duration,
                "pause_between_moves": pause_between_moves
            },
            "screenshot": {
                "key": screenshot_key,
                "delay": screenshot_delay,
                "pause": screenshot_pause
            },
            "controls": {}
        }

        # Control-specific configuration
        print(f"\n--- {control_type.title()} Control Settings ---")
        if control_type == "keyboard":
            print("Key configuration (use key names like 'left', 'right', 'up', 'down', 'a', 'w', etc.):")
            config["controls"]["keyboard"] = {
                "left": input("Left key [left]: ") or "left",
                "right": input("Right key [right]: ") or "right",
                "up": input("Up key [up]: ") or "up",
                "down": input("Down key [down]: ") or "down"
            }
        elif control_type == "gamepad":
            stick_movement = input(f"Stick movement amount (0.1-1.0) [{DEFAULT_GAMEPAD_STICK_MOVEMENT}]: ") or str(DEFAULT_GAMEPAD_STICK_MOVEMENT)
            config["controls"]["gamepad"] = {
                "stick_movement_amount": float(stick_movement)
            }
            print("Virtual gamepad support implemented using vgamepad!")
        elif control_type == "mouse":
            sensitivity = input(f"Mouse sensitivity in pixels (10-500) [{DEFAULT_MOUSE_SENSITIVITY}]: ") or str(DEFAULT_MOUSE_SENSITIVITY)
            capture_mouse = input("Capture mouse during operation? (y/n) [n]: ").lower()
            capture_mouse = capture_mouse == "y"
            config["controls"]["mouse"] = {
                "sensitivity": int(sensitivity),
                "capture_mouse": capture_mouse
            }
            print("Mouse control configured!")

        # Save configuration using config manager
        self.config_manager.add_game(game_name, config)
        self.config_manager.save()

        print(f"\nConfiguration saved for '{game_name}'!")
        print(f"Screenshot key: {screenshot_key}")
        print(f"Control type: {control_type}")
        print(f"Horizontal steps: {horizontal_steps}, Vertical steps: {vertical_steps}")

    def test_horizontal_rotation(self, game_name, game_config):
        """Test complete horizontal rotation to verify 360° coverage"""
        movement_config = game_config.get("movement", {})

        print(f"\n=== Testing Horizontal Rotation for '{game_name}' ===")
        print(f"Horizontal steps configured: {movement_config.get('horizontal_steps', DEFAULT_HORIZONTAL_STEPS)}")
        print(f"Horizontal movement duration: {movement_config.get('horizontal_movement_duration', DEFAULT_HORIZONTAL_MOVEMENT_DURATION)}s")
        print(f"Pause between moves: {movement_config.get('pause_between_moves', DEFAULT_PAUSE_BETWEEN_MOVES)}s")
        print("\nThis will perform a complete 360° horizontal rotation.")
        print("Watch the camera movement to see if it completes exactly one full rotation.")
        print("If it rotates too much or too little, adjust 'movement.horizontal_steps' in your config.")

        print(f"\nStarting test in {CAPTURE_COUNTDOWN_SECONDS} seconds...")
        print("Focus the game window now!")

        for i in range(CAPTURE_COUNTDOWN_SECONDS, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Horizontal Rotation Test ===")

        try:
            horizontal_steps = movement_config.get('horizontal_steps', DEFAULT_HORIZONTAL_STEPS)
            for step in range(horizontal_steps):
                print(f"Step {step + 1}/{horizontal_steps}")
                self.move_camera("right", game_config)

            print(f"\n=== Horizontal Test Complete ===")
            print("Did the camera complete exactly one full 360° rotation?")
            print("- If it rotated too much: DECREASE 'movement.horizontal_steps'")
            print("- If it didn't complete full rotation: INCREASE 'movement.horizontal_steps'")
            print("- If rotation was too fast/slow: adjust 'movement.horizontal_movement_duration' and 'movement.pause_between_moves'")

        except KeyboardInterrupt:
            print(f"\n=== Test Interrupted ===")

    def test_vertical_movement(self, game_name, game_config):
        """Test vertical movement from zenith to nadir"""
        movement_config = game_config.get("movement", {})

        print(f"\n=== Testing Vertical Movement for '{game_name}' ===")
        print(f"Vertical steps configured: {movement_config.get('vertical_steps', DEFAULT_VERTICAL_STEPS)}")
        print(f"Vertical movement duration: {movement_config.get('vertical_movement_duration', DEFAULT_VERTICAL_MOVEMENT_DURATION)}s")
        print(f"Pause between moves: {movement_config.get('pause_between_moves', DEFAULT_PAUSE_BETWEEN_MOVES)}s")
        print("\nThis will move the camera from zenith (straight up) to nadir (straight down).")
        print("Make sure your camera is positioned at zenith before starting!")
        print("Watch to see if it reaches exactly nadir (straight down) at the end.")

        print(f"\nStarting test in {CAPTURE_COUNTDOWN_SECONDS} seconds...")
        print("Focus the game window and position camera at ZENITH (straight up)!")

        for i in range(CAPTURE_COUNTDOWN_SECONDS, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Vertical Movement Test ===")

        try:
            vertical_steps = movement_config.get('vertical_steps', DEFAULT_VERTICAL_STEPS)
            for step in range(vertical_steps):
                print(f"Step {step + 1}/{vertical_steps}")
                self.move_camera("down", game_config)

            print(f"\n=== Vertical Test Complete ===")
            print("Did the camera reach exactly nadir (straight bottom)?")
            print("- If it went too far past nadir: DECREASE 'movement.vertical_steps'")
            print("- If it didn't reach nadir: INCREASE 'movement.vertical_steps'")
            print("- If movement was too fast/slow: adjust 'movement.vertical_movement_duration' and 'movement.pause_between_moves'")

        except KeyboardInterrupt:
            print(f"\n=== Test Interrupted ===")

    def calculate_capture_stats(self, game_name="default"):
        """Calculate and display capture statistics (screenshots count and estimated time)"""
        if not self.config_manager.has_game(game_name):
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config_manager.get_game_config(game_name)
        movement_config = game_config.get("movement", {})
        screenshot_config = game_config.get("screenshot", {})

        # Calculate total screenshots
        horizontal_steps = movement_config["horizontal_steps"]
        vertical_steps = movement_config["vertical_steps"]
        total_screenshots = horizontal_steps * (vertical_steps + 1)

        # Calculate timing components (in seconds)
        horizontal_movement_duration = movement_config.get("horizontal_movement_duration", DEFAULT_HORIZONTAL_MOVEMENT_DURATION)
        vertical_movement_duration = movement_config.get("vertical_movement_duration", DEFAULT_VERTICAL_MOVEMENT_DURATION)
        pause_between_moves = movement_config.get("pause_between_moves", DEFAULT_PAUSE_BETWEEN_MOVES)
        screenshot_delay = screenshot_config.get("delay", DEFAULT_SCREENSHOT_DELAY)
        screenshot_pause = screenshot_config.get("pause", DEFAULT_SCREENSHOT_PAUSE)

        # Time calculations
        # For each screenshot: screenshot_delay + screenshot_pause
        screenshot_time = total_screenshots * (screenshot_delay + screenshot_pause)

        # For horizontal movements: (horizontal_steps - 1) movements per vertical level
        horizontal_movements = (horizontal_steps - 1) * (vertical_steps + 1)
        horizontal_movement_time = horizontal_movements * (horizontal_movement_duration + pause_between_moves)

        # For vertical movements: vertical_steps movements total
        vertical_movements = vertical_steps
        vertical_movement_time = vertical_movements * (vertical_movement_duration + pause_between_moves)

        # Total time (plus 5 second countdown)
        total_time = screenshot_time + horizontal_movement_time + vertical_movement_time + 5

        print(f"\n=== Capture Statistics for '{game_name}' ===")
        print(f"Configuration:")
        print(f"  Horizontal steps: {horizontal_steps}")
        print(f"  Vertical steps: {vertical_steps}")
        print(f"  Control type: {game_config['control_type']}")
        print(f"  Screenshot key: {game_config.get('screenshot_key', 'f9')}")

        print(f"\nTiming settings:")
        print(f"  Horizontal movement duration: {horizontal_movement_duration}s")
        print(f"  Vertical movement duration: {vertical_movement_duration}s")
        print(f"  Pause between moves: {pause_between_moves}s")
        print(f"  Screenshot delay: {screenshot_delay}s")
        print(f"  Screenshot pause: {screenshot_pause}s")

        print(f"\nCapture statistics:")
        print(f"  Total screenshots: {total_screenshots}")
        print(f"  Horizontal movements: {horizontal_movements}")
        print(f"  Vertical movements: {vertical_movements}")

        print(f"\nEstimated time breakdown:")
        print(f"  Initial countdown: 5s")
        print(f"  Screenshot time: {screenshot_time:.1f}s")
        print(f"  Horizontal movement time: {horizontal_movement_time:.1f}s")
        print(f"  Vertical movement time: {vertical_movement_time:.1f}s")
        print(f"  Total estimated time: {total_time:.1f}s ({total_time/60:.1f} minutes)")

        print(f"\nCapture pattern:")
        print(f"  Start position: Zenith (straight up)")
        print(f"  End position: Nadir (straight down)")
        print(f"  Pattern: {vertical_steps + 1} horizontal rings, {horizontal_steps} shots per ring")

    def test_screenshot(self, game_name="default"):
        """Test screenshot tool functionality"""
        if not self.config_manager.has_game(game_name):
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config_manager.get_game_config(game_name)
        screenshot_config = game_config.get("screenshot", {})
        screenshot_key = screenshot_config.get("key", "f9")

        print(f"\n=== Testing Screenshot Tool for '{game_name}' ===")
        print(f"Screenshot key configured: {screenshot_key}")
        print(f"Screenshot delay: {screenshot_config.get('delay', DEFAULT_SCREENSHOT_DELAY)}s")
        print(f"Screenshot pause: {screenshot_config.get('pause', DEFAULT_SCREENSHOT_PAUSE)}s")
        print("\nThis will test your screenshot tool by taking 3 test screenshots.")
        print("Make sure:")
        print("- Your screenshot tool is running and ready")
        print("- The game window is in focus")
        print("- Your screenshot region/settings are configured")

        print(f"\nStarting screenshot test in {CAPTURE_COUNTDOWN_SECONDS} seconds...")
        print("Focus the game window now!")

        for i in range(CAPTURE_COUNTDOWN_SECONDS, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Screenshot Test ===")

        try:
            for test_num in range(1, 4):
                print(f"Taking test screenshot {test_num}/3...")

                # Take screenshot using configured keybind
                time.sleep(screenshot_config.get("delay", DEFAULT_SCREENSHOT_DELAY))
                if self.take_screenshot(test_num, game_config):
                    print(f"✓ Screenshot {test_num} triggered successfully")
                else:
                    print(f"✗ Screenshot {test_num} failed")

                # Wait between screenshots
                if test_num < 3:
                    time.sleep(2)

            print(f"\n=== Screenshot Test Complete ===")
            print("Check your screenshot tool's output folder for the 3 test images.")
            print("If screenshots didn't capture properly:")
            print(f"- Verify your screenshot tool responds to '{screenshot_key}' key")
            print("- Check if the game window was in focus")
            print("- Ensure your screenshot tool's region is set correctly")
            print("- Try adjusting screenshot_delay and screenshot_pause in config")

        except KeyboardInterrupt:
            print(f"\n=== Screenshot Test Interrupted ===")

    def test_movement(self, game_name="default", test_type="horizontal"):
        """Test camera movement patterns for fine-tuning"""
        if not self.config_manager.has_game(game_name):
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config_manager.get_game_config(game_name)

        if test_type == "horizontal":
            self.test_horizontal_rotation(game_name, game_config)
        elif test_type == "vertical":
            self.test_vertical_movement(game_name, game_config)
        else:
            print("Invalid test type. Use 'horizontal' or 'vertical'.")


def main():
    parser = argparse.ArgumentParser(description="360° Game Screenshot Automation")
    parser.add_argument("--setup", help="Setup configuration for a game")
    parser.add_argument("--capture", help="Capture panorama for specified game")
    parser.add_argument("--test-horizontal", help="Test horizontal 360° rotation for specified game")
    parser.add_argument("--test-vertical", help="Test vertical zenith to nadir movement for specified game")
    parser.add_argument("--test-screenshot", help="Test screenshot tool functionality for specified game")
    parser.add_argument("--calculate", help="Calculate and display capture statistics for specified game")
    parser.add_argument("--list", action="store_true", help="List configured games")

    args = parser.parse_args()

    capturer = GamePanoCapture()

    if args.setup:
        capturer.create_game_config(args.setup)
    elif args.capture:
        capturer.capture_panorama(args.capture)
    elif args.test_horizontal:
        capturer.test_movement(args.test_horizontal, "horizontal")
    elif args.test_vertical:
        capturer.test_movement(args.test_vertical, "vertical")
    elif args.test_screenshot:
        capturer.test_screenshot(args.test_screenshot)
    elif args.calculate:
        capturer.calculate_capture_stats(args.calculate)
    elif args.list:
        print("Configured games:")
        for game in capturer.config_manager.list_games():
            print(f"  - {game}")
    else:
        print("360° Game Screenshot Automation")
        print("Usage examples:")
        print("  python3 pano_capture.py --setup 'My Game'              # Setup new game config")
        print("  python3 pano_capture.py --capture 'My Game'            # Capture panorama")
        print("  python3 pano_capture.py --test-horizontal 'My Game'    # Test horizontal (360°) rotation")
        print("  python3 pano_capture.py --test-vertical 'My Game'      # Test vertical (zenith to nadir) movement")
        print("  python3 pano_capture.py --test-screenshot 'My Game'    # Test screenshot tool functionality")
        print("  python3 pano_capture.py --calculate 'My Game'          # Calculate capture statistics and time")
        print("  python3 pano_capture.py --list                         # List configured games")


if __name__ == "__main__":
    main()
