# Game 360° Panorama Capture Automation

## Repository Structure

```
game-360-panorama-capture/
├── pano_capture.py           # Main automation script
├── requirements.txt               # Required Python packages
├── game_config.json               # Game-specific configurations
├── captures/                      # Capture sessions are stored here
│   └── panorama_capture_[game]_[timestamp]/
│       ├── session_info.json     # Capture session metadata
│       └── (screenshots saved by your capture tool)
└── README.md                      # This documentation file
```

## Prerequisites

- Python 3.7 or higher
- A screenshot/region capture tool (e.g., ShareX, Greenshot, etc.)
- Video games with photo mode capability

### Install Python

If you don't have Python installed:

```bash
# Using package manager on various systems
# Windows: Download from python.org
# macOS: 
brew install python
# Linux (Ubuntu/Debian):
sudo apt install python3 python3-pip
```

Verify the installation:
```bash
python3 --version
```

### Set Up Virtual Environment

```bash
# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

## Game Panorama Capture

### Overview

Game 360° Panorama Capture is an automation tool that captures spherical panoramic screenshots from video games with photo modes. It systematically moves the camera in a spherical pattern and triggers your screenshot tool to capture images suitable for creating equirectangular panoramas.

### Features

- **Game-specific configurations**: Each game can have unique camera movement and timing settings
- **Flexible control support**: Works with keyboard controls or gamepad (Xbox controller/similar)
- **Custom screenshot integration**: Uses your preferred screenshot tool via configurable keybinds
- **Spherical capture pattern**: Follows proper panoramic photography patterns from nadir to zenith
- **Resume capability**: Can be interrupted and provides partial capture information
- **Movement testing**: Test camera movement and screenshot triggers before full capture

### Usage

#### 1. Initial Setup for a New Game

Configure a new game with its specific settings:

```bash
python3 pano_capture.py --setup "Cyberpunk 2077"
```

You'll be prompted to configure:
- Control type (keyboard/gamepad)
- Camera movement keys
- Screenshot keybind for your capture tool
- Movement timing and delays
- Spherical capture parameters (horizontal/vertical steps)

#### 2. Test Configuration

Before doing a full capture, test your settings:

```bash
# Test horizontal rotation (360° test)
python3 pano_capture.py --test-horizontal "Cyberpunk 2077"

# Test vertical movement (nadir to zenith)
python3 pano_capture.py --test-vertical "Cyberpunk 2077"
```

These tests will verify camera movement works correctly before doing a full capture.

#### 3. Capture a Panorama

Once configured and tested:

```bash
python3 pano_capture.py --capture "Cyberpunk 2077"
```

### Capture Workflow

1. **Prepare the game**:
    - Open your game and navigate to desired location
    - Enter photo mode
    - Position camera at nadir (looking straight down)
    - Ensure your screenshot tool is ready

2. **Start capture**:
    - Run the capture command
    - Focus the game window during the 5-second countdown
    - Let the script automatically handle camera movement and screenshots

3. **Process results**:
    - Screenshots are saved by your capture tool
    - Session information is saved in the captures directory
    - Use software like Autogiga Pano to create equirectangular panorama

### Configuration Parameters

#### Movement Settings
- `movement_duration`: How long to hold movement keys (seconds)
- `pause_between_moves`: Delay between camera movements (seconds)
- `screenshot_delay`: Wait time before taking screenshot (seconds)
- `screenshot_pause`: Wait time after taking screenshot (seconds)

#### Capture Pattern
- `horizontal_steps`: Number of steps for complete horizontal rotation (your "magic number")
- `vertical_steps`: Number of steps from nadir to zenith

#### Controls
- `control_type`: "keyboard" or "gamepad"
- `keys`: Mapping of directions to keyboard keys
- `screenshot_key`: Key combination for your screenshot tool

### Example Configuration

```json
{
  "games": {
    "Cyberpunk 2077": {
      "control_type": "keyboard",
      "screenshot_key": "f9",
      "keys": {
        "left": "left",
        "right": "right",
        "up": "up",
        "down": "down"
      },
      "movement_duration": 0.1,
      "pause_between_moves": 0.3,
      "screenshot_delay": 0.5,
      "screenshot_pause": 0.8,
      "horizontal_steps": 36,
      "vertical_steps": 18
    }
  }
}
```

### Advanced Configuration

#### Custom Key Bindings

The script supports various key formats:
- Simple keys: `f9`, `space`, `enter`
- Arrow keys: `left`, `right`, `up`, `down`
- Letter keys: `w`, `a`, `s`, `d`
- Key combinations: `ctrl+shift+s`, `alt+f12`

#### Gamepad Configuration

```json
{
  "games": {
    "Cyberpunk 2077 (Gamepad)": {
      "control_type": "gamepad",
      "screenshot_key": "f9",
      "gamepad": {
        "stick_movement_amount": 0.8,
        "gamepad_index": 0
      },
      "movement_duration": 0.1,
      "pause_between_moves": 0.3,
      "screenshot_delay": 0.5,
      "screenshot_pause": 0.8,
      "horizontal_steps": 36,
      "vertical_steps": 18
    }
  }
}
```

**Gamepad Settings:**
- `stick_movement_amount`: How far to move the right stick (0.1-1.0)
- Uses the right analog stick for camera movement

#### Screenshot Tool Integration

Popular screenshot tools and their typical keybinds:
- **ShareX**: `ctrl+shift+4` (region capture)
- **Greenshot**: `printscreen` or custom hotkey
- **Windows Snipping Tool**: `win+shift+s`
- **macOS Screenshot**: `cmd+shift+4`

### Command Reference

```bash
# Setup new game configuration
python3 pano_capture.py --setup "Game Name"

# Capture panorama for configured game
python3 pano_capture.py --capture "Game Name"

# Test horizontal rotation (360° test)
python3 pano_capture.py --test-horizontal "Game Name"

# Test vertical movement (nadir to zenith)
python3 pano_capture.py --test-vertical "Game Name"

# List all configured games
python3 pano_capture.py --list
```

## Complete Workflow

Follow these steps to create a 360° panorama from a video game:

### 1. **Initial Setup**
```bash
# Configure your game
python3 pano_capture.py --setup "My Favorite Game"
```

### 2. **Test Configuration**
```bash
# Test horizontal rotation (360° test)
python3 pano_capture.py --test-horizontal "My Favorite Game"

# Test vertical movement (nadir to zenith)
python3 pano_capture.py --test-vertical "My Favorite Game"
```

### 3. **Prepare Game Environment**
- Launch your game
- Navigate to the desired location
- Setup your capture region in your screenshot tool
- Enter photo mode
- Position camera at zenith (straight up)

### 4. **Capture Session**
```bash
# Start automated capture
python3 pano_capture.py --capture "My Favorite Game"
```

### 5. **Create Panorama**
- Locate screenshots in your capture tool's output folder
- Import images into panorama software (e.g., Autogiga Pano)
- Process into equirectangular format
- View your 360° panorama!

### Tips for Best Results

#### Camera Positioning
- Always start at zenith (straight up) for consistent results
- Ensure the game's camera center point is stable

#### Movement Calibration
- Fine-tune `horizontal_steps` to ensure complete coverage without gaps
- Adjust `vertical_steps` based on the game's vertical field of view
- Use test mode to verify smooth camera movement

#### Screenshot Quality
- Configure your screenshot tool for highest quality
- Ensure consistent region capture (same area every time)
- Consider using lossless formats (PNG) for best stitching results

### Troubleshooting

- **Camera moves too fast/slow**: Adjust `movement_duration` and `pause_between_moves`
- **Screenshots not capturing**: Verify `screenshot_key` matches your tool's hotkey
- **Missing coverage areas**: Increase `horizontal_steps` or `vertical_steps`
- **Game loses focus**: Ensure game window stays active during capture
- **Inconsistent movement**: Some games may need longer delays or different key mappings

### Windows Virtual Gamepad Support

For gamepad control on Windows, the script uses `vgamepad` to create a virtual Xbox 360 controller:

```bash
pip install vgamepad
```

**Note**: Virtual gamepad functionality is Windows-only. On other platforms, use keyboard control.

### Future Enhancements

Planned features for future versions:
- Automatic panorama stitching integration
- HDR capture support for compatible games
- Cross-platform gamepad support
