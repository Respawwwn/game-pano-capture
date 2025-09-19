#!/usr/bin/env python3
"""
360° Game Screenshot Automation Script
Automates the capture of panoramic screenshots from video games for photosphere creation.
Uses configurable keybinds to trigger external screenshot tools.
"""

import time
import os
import json
from datetime import datetime
from pathlib import Path
import keyboard
import argparse
import pygame
import vgamepad as vg

class GamePanoCapture:
    def __init__(self, config_file="game_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.screenshot_count = 0
        self.output_dir = None
        self.gamepad = None
        self.gamepad_initialized = False
        self.virtual_gamepad = None

    def load_config(self):
        """Load or create configuration file"""
        default_config = {
            "games": {
                "default": {
                    "control_type": "keyboard",  # "keyboard" or "gamepad"
                    "keys": {
                        "left": "left",
                        "right": "right",
                        "up": "up",
                        "down": "down"
                    },
                    "gamepad": {
                        "stick_movement_amount": 0.8  # Amount to move stick (0.0 to 1.0)
                    },
                    "screenshot_key": "f9",  # Key combination for taking screenshots
                    "movement_duration": 0.1,  # Duration to hold key/stick
                    "pause_between_moves": 0.3,  # Pause between movements
                    "screenshot_delay": 0.5,  # Delay after movement before screenshot
                    "screenshot_pause": 0.8,  # Pause after taking screenshot
                    "horizontal_steps": 36,  # Number of steps for complete horizontal rotation
                    "vertical_steps": 18     # Number of steps from nadir to zenith
                }
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                print(f"Error reading config file. Using defaults.")
                return default_config
        else:
            # Create default config file
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {self.config_file}")
            return default_config

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

        try:
            # Create virtual Xbox 360 gamepad
            self.virtual_gamepad = vg.VX360Gamepad()
            print("Virtual Xbox 360 gamepad created successfully")
            self.gamepad_initialized = True
            return True

        except Exception as e:
            print(f"Error initializing virtual gamepad: {e}")
            return False

    def take_screenshot(self, screenshot_number, game_config):
        """Trigger screenshot using configured keybind"""
        try:
            screenshot_key = game_config.get("screenshot_key", "f9")
            print(f"Taking screenshot {screenshot_number:04d} (pressing {screenshot_key})...")

            # Handle key combinations (e.g., "ctrl+shift+f9", "alt+1")
            if "+" in screenshot_key:
                keys = screenshot_key.split("+")
                # Use keyboard.press_and_release for better Windows compatibility
                keyboard.press_and_release(screenshot_key)
            else:
                keyboard.press_and_release(screenshot_key)

            # Wait for screenshot to be processed by external tool
            time.sleep(game_config.get("screenshot_pause", 0.8))
            return True
        except Exception as e:
            print(f"Error triggering screenshot: {e}")
            return False

    def move_camera(self, direction, game_config):
        """Move camera in specified direction"""
        if game_config["control_type"] == "keyboard":
            key = game_config["keys"][direction]
            keyboard.press(key)
            time.sleep(game_config["movement_duration"])
            keyboard.release(key)
        elif game_config["control_type"] == "gamepad":
            if not self.init_gamepad(game_config):
                print("Error: Could not initialize gamepad")
                return

            # Get movement amount from config
            stick_amount = game_config.get("gamepad", {}).get("stick_movement_amount", 0.8)
            movement_duration = game_config["movement_duration"]

            # Map directions to right stick movements
            if direction == "right":
                x_axis = stick_amount
                y_axis = 0.0
            elif direction == "left":
                x_axis = -stick_amount
                y_axis = 0.0
            elif direction == "up":
                x_axis = 0.0
                y_axis = -stick_amount  # Negative Y is up on most game right sticks
            elif direction == "down":
                x_axis = 0.0
                y_axis = stick_amount   # Positive Y is down on most game right sticks
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

        time.sleep(game_config["pause_between_moves"])

    def capture_panorama(self, game_name="default"):
        """Main capture routine"""
        if game_name not in self.config["games"]:
            print(f"Game '{game_name}' not found in config. Using default.")
            game_name = "default"

        game_config = self.config["games"][game_name]

        # Initialize gamepad if needed
        if game_config["control_type"] == "gamepad":
            if not self.init_gamepad(game_config):
                print("Failed to initialize gamepad. Aborting capture.")
                return

        print(f"\n=== 360° Panorama Capture Started ===")
        print(f"Game: {game_name}")
        print(f"Horizontal steps: {game_config['horizontal_steps']}")
        print(f"Vertical steps: {game_config['vertical_steps']}")
        print(f"Control type: {game_config['control_type']}")
        print(f"Screenshot key: {game_config.get('screenshot_key', 'f9')}")

        print(f"\nStarting capture in 5 seconds...")
        print("Make sure the game is in focus and camera is at zenith position (straight up)!")
        print("Make sure your screenshot tool is ready!")
        print(f"Screenshot key: {game_config.get('screenshot_key', 'f9')}")
        print("Press Ctrl+C to abort at any time.")

        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        self.setup_output_directory(game_name)
        self.screenshot_count = 0

        try:
            # Start from zenith and work downwards
            for vertical_step in range(game_config["vertical_steps"] + 1):
                print(f"\nVertical level {vertical_step + 1}/{game_config['vertical_steps'] + 1}")

                # Take screenshots for complete horizontal rotation
                for horizontal_step in range(game_config["horizontal_steps"]):
                    # Take screenshot using configured keybind
                    time.sleep(game_config["screenshot_delay"])
                    if self.take_screenshot(self.screenshot_count + 1, game_config):
                        self.screenshot_count += 1

                    # Move right (except on last horizontal step)
                    if horizontal_step < game_config["horizontal_steps"] - 1:
                        self.move_camera("right", game_config)

                # Move down for next vertical level (except on last vertical step)
                if vertical_step < game_config["vertical_steps"]:
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
                "expected_screenshots": game_config["horizontal_steps"] * (game_config["vertical_steps"] + 1),
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
                "expected_screenshots": game_config["horizontal_steps"] * (game_config["vertical_steps"] + 1)
            }
            with open(self.output_dir / "session_info.json", 'w') as f:
                json.dump(session_info, f, indent=4)

    def create_game_config(self, game_name):
        """Interactive setup for a new game configuration"""
        print(f"\n=== Setting up configuration for '{game_name}' ===")

        # Control type
        control_type = input("Control type (keyboard/gamepad) [keyboard]: ").lower()
        if control_type not in ["keyboard", "gamepad"]:
            control_type = "keyboard"

        config = {
            "control_type": control_type,
            "screenshot_key": input("Screenshot keybind (e.g., 'f9', 'ctrl+shift+s', 'alt+4') [f9]: ") or "f9",
            "movement_duration": float(input("Movement duration in seconds [0.1]: ") or "0.1"),
            "pause_between_moves": float(input("Pause between moves in seconds [0.3]: ") or "0.3"),
            "screenshot_delay": float(input("Delay before screenshot in seconds [0.5]: ") or "0.5"),
            "screenshot_pause": float(input("Pause after screenshot in seconds [0.8]: ") or "0.8"),
            "horizontal_steps": int(input("Horizontal steps for complete rotation [36]: ") or "36"),
            "vertical_steps": int(input("Vertical steps from zenith to nadir [18]: ") or "18")
        }

        if control_type == "keyboard":
            print("Key configuration (use key names like 'left', 'right', 'up', 'down', 'a', 'w', etc.):")
            config["keys"] = {
                "left": input("Left key [left]: ") or "left",
                "right": input("Right key [right]: ") or "right",
                "up": input("Up key [up]: ") or "up",
                "down": input("Down key [down]: ") or "down"
            }
        else:
            stick_movement = input("Stick movement amount (0.1-1.0) [0.8]: ") or "0.8"

            config["gamepad"] = {
                "stick_movement_amount": float(stick_movement)
            }
            print("Virtual gamepad support implemented using vgamepad!")

        # Save configuration
        self.config["games"][game_name] = config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

        print(f"Configuration saved for '{game_name}'!")
        print(f"Screenshot key configured: {config['screenshot_key']}")

    def test_horizontal_rotation(self, game_name, game_config):
        """Test complete horizontal rotation to verify 360° coverage"""
        print(f"\n=== Testing Horizontal Rotation for '{game_name}' ===")
        print(f"Horizontal steps configured: {game_config['horizontal_steps']}")
        print(f"Movement duration: {game_config['movement_duration']}s")
        print(f"Pause between moves: {game_config['pause_between_moves']}s")
        print("\nThis will perform a complete 360° horizontal rotation.")
        print("Watch the camera movement to see if it completes exactly one full rotation.")
        print("If it rotates too much or too little, adjust 'horizontal_steps' in your config.")

        print(f"\nStarting test in 5 seconds...")
        print("Focus the game window now!")

        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Horizontal Rotation Test ===")

        try:
            for step in range(game_config["horizontal_steps"]):
                print(f"Step {step + 1}/{game_config['horizontal_steps']}")
                self.move_camera("right", game_config)

            print(f"\n=== Horizontal Test Complete ===")
            print("Did the camera complete exactly one full 360° rotation?")
            print("- If it rotated too much: DECREASE 'horizontal_steps'")
            print("- If it didn't complete full rotation: INCREASE 'horizontal_steps'")
            print("- If rotation was too fast/slow: adjust 'movement_duration' and 'pause_between_moves'")

        except KeyboardInterrupt:
            print(f"\n=== Test Interrupted ===")

    def test_vertical_movement(self, game_name, game_config):
        """Test vertical movement from zenith to nadir"""
        print(f"\n=== Testing Vertical Movement for '{game_name}' ===")
        print(f"Vertical steps configured: {game_config['vertical_steps']}")
        print(f"Movement duration: {game_config['movement_duration']}s")
        print(f"Pause between moves: {game_config['pause_between_moves']}s")
        print("\nThis will move the camera from zenith (straight up) to nadir (straight down).")
        print("Make sure your camera is positioned at zenith before starting!")
        print("Watch to see if it reaches exactly nadir (straight down) at the end.")

        print(f"\nStarting test in 5 seconds...")
        print("Focus the game window and position camera at ZENITH (straight up)!")

        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Vertical Movement Test ===")

        try:
            for step in range(game_config["vertical_steps"]):
                print(f"Step {step + 1}/{game_config['vertical_steps']}")
                self.move_camera("up", game_config)

            print(f"\n=== Vertical Test Complete ===")
            print("Did the camera reach exactly zenith (straight up)?")
            print("- If it went too far past zenith: DECREASE 'vertical_steps'")
            print("- If it didn't reach zenith: INCREASE 'vertical_steps'")
            print("- If movement was too fast/slow: adjust 'movement_duration' and 'pause_between_moves'")

        except KeyboardInterrupt:
            print(f"\n=== Test Interrupted ===")

    def calculate_capture_stats(self, game_name="default"):
        """Calculate and display capture statistics (screenshots count and estimated time)"""
        if game_name not in self.config["games"]:
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config["games"][game_name]

        # Calculate total screenshots
        horizontal_steps = game_config["horizontal_steps"]
        vertical_steps = game_config["vertical_steps"]
        total_screenshots = horizontal_steps * (vertical_steps + 1)

        # Calculate timing components (in seconds)
        movement_duration = game_config["movement_duration"]
        pause_between_moves = game_config["pause_between_moves"]
        screenshot_delay = game_config.get("screenshot_delay", 0.5)
        screenshot_pause = game_config.get("screenshot_pause", 0.8)

        # Time calculations
        # For each screenshot: screenshot_delay + screenshot_pause
        screenshot_time = total_screenshots * (screenshot_delay + screenshot_pause)

        # For horizontal movements: (horizontal_steps - 1) movements per vertical level
        horizontal_movements = (horizontal_steps - 1) * (vertical_steps + 1)
        horizontal_movement_time = horizontal_movements * (movement_duration + pause_between_moves)

        # For vertical movements: vertical_steps movements total
        vertical_movements = vertical_steps
        vertical_movement_time = vertical_movements * (movement_duration + pause_between_moves)

        # Total time (plus 5 second countdown)
        total_time = screenshot_time + horizontal_movement_time + vertical_movement_time + 5

        print(f"\n=== Capture Statistics for '{game_name}' ===")
        print(f"Configuration:")
        print(f"  Horizontal steps: {horizontal_steps}")
        print(f"  Vertical steps: {vertical_steps}")
        print(f"  Control type: {game_config['control_type']}")
        print(f"  Screenshot key: {game_config.get('screenshot_key', 'f9')}")

        print(f"\nTiming settings:")
        print(f"  Movement duration: {movement_duration}s")
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
        if game_name not in self.config["games"]:
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config["games"][game_name]
        screenshot_key = game_config.get("screenshot_key", "f9")

        print(f"\n=== Testing Screenshot Tool for '{game_name}' ===")
        print(f"Screenshot key configured: {screenshot_key}")
        print(f"Screenshot delay: {game_config.get('screenshot_delay', 0.5)}s")
        print(f"Screenshot pause: {game_config.get('screenshot_pause', 0.8)}s")
        print("\nThis will test your screenshot tool by taking 3 test screenshots.")
        print("Make sure:")
        print("- Your screenshot tool is running and ready")
        print("- The game window is in focus")
        print("- Your screenshot region/settings are configured")

        print(f"\nStarting screenshot test in 5 seconds...")
        print("Focus the game window now!")

        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\n=== Starting Screenshot Test ===")

        try:
            for test_num in range(1, 4):
                print(f"Taking test screenshot {test_num}/3...")

                # Take screenshot using configured keybind
                time.sleep(game_config.get("screenshot_delay", 0.5))
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
        if game_name not in self.config["games"]:
            print(f"Game '{game_name}' not found in config.")
            return

        game_config = self.config["games"][game_name]

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
        for game in capturer.config["games"]:
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
