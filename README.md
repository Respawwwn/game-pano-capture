# Game 360° Panorama Capture Automation

Game 360° Panorama Capture is an automation tool that captures spherical panoramic screenshots from video games with photo modes.
It systematically moves the camera in a spherical pattern and triggers your screenshot tool to capture images suitable for creating equirectangular panoramas.

> This tool captures individual screenshots - you must use panorama stitching software to create the final equirectangular panorama.

## Features

- **Game-specific configurations**: Each game can have unique camera movement and timing settings
- **Multiple control support**: Works with keyboard, gamepad (Xbox controller), or mouse controls
- **Custom screenshot integration**: Uses your preferred screenshot tool via configurable keybinds
- **Spherical capture pattern**: Follows proper panoramic photography patterns from zenith to nadir
- **Resume capability**: Can be interrupted and provides partial capture information
- **Movement testing**: Test camera movement and screenshot triggers before full capture
- **Separate horizontal/vertical timing**: Independent movement durations for precise control

## Prerequisites

- Python 3.7 or higher
- A screenshot/region capture tool (e.g., ShareX, Greenshot, etc.)
- Video games with photo mode capability

## Getting Started

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

```bash
# Install required packages.
pip install -r requirements.txt
```

```bash
# Setup a game.
python pano_capture.py --setup "Cyberpunk 2077"
# Capture a panorama.
python pano_capture.py --capture "Cyberpunk 2077"
```

Before doing a full capture, test your settings:

```bash
# Test horizontal rotation (360° test).
python pano_capture.py --test-horizontal "Cyberpunk 2077"

# Test vertical movement (nadir to zenith).
python pano_capture.py --test-vertical "Cyberpunk 2077"

# Test screenshot keybind.
python pano_capture.py --test-screenshot "Cyberpunk 2077"
```

## Install Python

If you don't have Python installed:

```bash
# Using package manager on various systems
# Windows: Download from python.org
# macOS: 
brew install python
# Linux (Ubuntu/Debian):
sudo apt install python python-pip
```

Verify the installation:
```bash
python --version
```

## Usage

### 1. Initial Setup for a New Game

Configure a new game with its specific settings:

```bash
python pano_capture.py --setup "Cyberpunk 2077"
```

You'll be prompted to configure:
- Control type (keyboard/gamepad/mouse)
- Screenshot settings (keybind, delay, pause)
- Movement settings (steps, duration, pause)
- Control-specific settings (keys, gamepad sensitivity, mouse sensitivity)

### 2. **Prepare Game Environment**
- Launch your game
- Navigate to the desired location
- Setup your capture region in your screenshot tool
- Enter photo mode
- Position camera at zenith (straight up)

### 3. Test Configuration

Before doing a full capture, test your settings:

```bash
# Test horizontal rotation (360° test)
python pano_capture.py --test-horizontal "Cyberpunk 2077"

# Test vertical movement (nadir to zenith)
python pano_capture.py --test-vertical "Cyberpunk 2077"

# Test screenshot keybind
python pano_capture.py --test-screenshot "Cyberpunk 2077"
```

These tests will verify camera movement works correctly before doing a full capture.

### 3. Capture a Panorama

Once configured and tested:

```bash
# Start automated capture
python pano_capture.py --capture "Cyberpunk 2077"
```

### 4. **Create Panorama**
- Locate screenshots in your capture tool's output folder
- Import images into panorama software (e.g., Autogiga Pano)
- Process into equirectangular format
- View your 360° panorama!

## Configuration Parameters

### Movement Settings
- `movement.horizontal_steps`: Number of steps for complete horizontal rotation
- `movement.vertical_steps`: Number of steps from zenith to nadir
- `movement.horizontal_movement_duration`: How long to hold horizontal movement (seconds)
- `movement.vertical_movement_duration`: How long to hold vertical movement (seconds)
- `movement.pause_between_moves`: Delay between camera movements (seconds)

### Screenshot Settings
- `screenshot_type`: "external_app" (uses external tool) or "built_in" (direct capture)
- `screenshot.shortcut_key`: Key combination for external screenshot tool (external_app only)
- `screenshot.delay`: Wait time before taking screenshot (seconds)
- `screenshot.pause`: Wait time after taking screenshot (seconds)
- `screenshot.monitor`: Monitor number to capture from (built_in only, 1-based index)
- `screenshot.path`: Directory path to save screenshots (built_in only)

### Control Settings
- `control_type`: "keyboard", "gamepad", or "mouse"
- `controls.keyboard`: Mapping of directions to keyboard keys
- `controls.gamepad.stick_movement_amount`: Gamepad sensitivity (0.1-1.0)
- `controls.mouse.sensitivity`: Mouse movement pixels (10-500)

### Example Configurations

#### Custom Key Bindings

The script supports various key formats:
- Simple keys: `f9`, `space`, `enter`
- Arrow keys: `left`, `right`, `up`, `down`
- Letter keys: `w`, `a`, `s`, `d`
- Key combinations: `ctrl+shift+s`, `alt+f12`

#### Keyboard Control
```json
{
  "games": {
    "Cyberpunk 2077": {
      "control_type": "keyboard",
      "movement": {
        "horizontal_steps": 36,
        "vertical_steps": 18,
        "horizontal_movement_duration": 0.1,
        "vertical_movement_duration": 0.1,
        "pause_between_moves": 0.3
      },
      "controls": {
        "keyboard": {
          "left": "left",
          "right": "right",
          "up": "up",
          "down": "down"
        }
      }
    }
  }
}
```

**Control Settings:**
- `left` the key to move the camera left
- `right` the key to move the camera right
- `up` the key to move the camera up
- `down` the key to move the camera down

#### Gamepad Configuration

```json
{
  "games": {
    "Cyberpunk 2077 (Gamepad)": {
      "control_type": "gamepad",
      "movement": {
        "horizontal_steps": 36,
        "vertical_steps": 18,
        "horizontal_movement_duration": 0.1,
        "vertical_movement_duration": 0.1,
        "pause_between_moves": 0.3
      },
      "controls": {
        "gamepad": {
          "stick_movement_amount": 0.8
        }
      },
    }
  }
}
```

**Control Settings:**
- `stick_movement_amount` controls how far to move the right stick (0.1-1.0)

#### Mouse Configuration

```json
{
  "games": {
    "Cyberpunk 2077 (Mouse)": {
      "control_type": "mouse",
      "movement": {
        "horizontal_steps": 36,
        "vertical_steps": 18,
        "horizontal_movement_duration": 0.1,
        "vertical_movement_duration": 0.1,
        "pause_between_moves": 0.3
      },
      "controls": {
        "mouse": {
          "sensitivity": 200,
        }
      },
    }
  }
}
```

**Control Settings:**
- `sensitivity` controls mouse movement distance in pixels (10-500)

#### Screenshot Configuration

```json
{
  "games": {
    "Cyberpunk 2077 (Screenshot External App)": {
      "screenshot_type": "external_app",
      "screenshot": {
        "shortcut_key": "f9",
        "delay": 0.5,
        "pause": 0.8
      },
    }
  }
}
```

```json
{
  "games": {
    "Cyberpunk 2077 (Screenshot Built-in)": {
      "screenshot_type": "built_in",
      "screenshot": {
         "delay": 0.5,
         "pause": 0.8,
         "monitor": 1,
         "path": "./screenshots/"
      },
    }
  }
}
```

**Control Settings:**
- `shortcut_key` the key combination to trigger your screenshot tool
- `delay` seconds to wait before taking screenshot (to allow camera to stabilize and game assets to load)
- `pause` seconds to wait after taking screenshot (to avoid overwhelming the screenshot tool)
- `monitor` monitor number to capture from (1-based index)
- `path` screenshot save directory 

## Command Reference

```bash
# Setup new game configuration
python pano_capture.py --setup "Game Name"

# Capture panorama for configured game
python pano_capture.py --capture "Game Name"

# Test horizontal rotation (360° test)
python pano_capture.py --test-horizontal "Game Name"

# Test vertical movement (nadir to zenith)
python pano_capture.py --test-vertical "Game Name"

# Test screenshot keybind
python pano_capture.py --test-screenshot "Game Name"

# List all configured games
python pano_capture.py --list
```

## Tips for Best Results

### Camera Positioning
- Always start at zenith (straight up) for consistent results
- Ensure the game's camera center point is stable

### Movement Calibration
- Fine-tune `horizontal_steps` to ensure complete coverage without gaps
- Adjust `vertical_steps` based on the game's vertical field of view
- Use test mode to verify smooth camera movement

### Screenshot Quality
- Configure your screenshot tool for highest quality
- Ensure consistent region capture (same area every time)
- Avoid UI elements in the capture area

## Troubleshooting

- **Camera moves too fast/slow**: Adjust `movement_duration` and `pause_between_moves`
- **Motion blur in screenshots**: Increase `screenshot.delay` to allow camera stabilization
- **Unloaded game textures**: Pause longer before taking a screenshot `screenshot.pause`
- **Screenshots not capturing**: Verify `screenshot_key` matches your tool's hotkey
- **Missing coverage areas**: Increase `horizontal_steps` or `vertical_steps` to have overlapping shots
- **Inconsistent movement**: Some games may need longer delays or different key mappings

### Gamepad Support

Virtual gamepad functionality is Windows-only. On other platforms, use keyboard or mouse control.

### Screenshot Not Working When Game Has Focus

**Problem**: Screenshot hotkey works outside the game but fails when the game window is focused.

**Cause**: Fullscreen games often have higher priority and intercept keyboard input, preventing automation scripts from sending keystrokes.

**Solutions**:

1. **Run game in Windowed/Borderless mode** (Recommended)
   - Switch from fullscreen to windowed or borderless windowed mode
   - This allows external applications to send keyboard input

2. **Run Python script with elevated privileges**
   ```bash
   # Windows (run Command Prompt as Administrator)
   python pano_capture.py --test-screenshot "Your Game"
   
   # Linux/macOS
   sudo python pano_capture.py --test-screenshot "Your Game"
   ```

3. **Test with --test-screenshot first**
   ```bash
   python pano_capture.py --test-screenshot "Your Game"
   ```
   If it works outside the game but not inside, use solutions 1 or 2 above.
