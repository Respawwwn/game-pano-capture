"""
Windows gamepad handler implementation using vgamepad.

This handler provides Windows gamepad support using the vgamepad library
for virtual Xbox 360 controller simulation.
"""

import logging
import time
from .interface import IGamepadHandler

try:
    import vgamepad as vg
    VGAMEPAD_AVAILABLE = True
except ImportError:
    VGAMEPAD_AVAILABLE = False
    vg = None


class WindowsGamepadHandler(IGamepadHandler):
    """
    Windows gamepad handler using vgamepad for Xbox 360 controller simulation.
    
    This implementation uses the vgamepad library to create and control
    a virtual Xbox 360 gamepad on Windows systems.
    """
    
    def __init__(self):
        """Initialize the Windows gamepad handler."""
        self._logger = logging.getLogger(__name__)
        self._virtual_gamepad = None
        self._initialized = False
        
        if not VGAMEPAD_AVAILABLE:
            self._logger.warning("vgamepad not available for gamepad control")
    
    def initialize(self) -> bool:
        """
        Initialize the gamepad handler by creating a virtual Xbox 360 gamepad.
        
        Returns:
            True if successful, False otherwise
        """
        if self._initialized:
            return True
            
        if not VGAMEPAD_AVAILABLE:
            self._logger.error("vgamepad not available - gamepad support requires vgamepad package")
            return False
            
        try:
            # Create virtual Xbox 360 gamepad
            self._virtual_gamepad = vg.VX360Gamepad()
            self._initialized = True
            self._logger.info("Virtual Xbox 360 gamepad created successfully")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to initialize virtual gamepad: {e}")
            return False
    
    def move_stick(self, stick: str, x_value: float, y_value: float, duration: float) -> bool:
        """
        Move a gamepad stick to specified position for a duration.
        
        Args:
            stick: Stick to move ('left', 'right')
            x_value: X-axis value (-1.0 to 1.0, negative = left, positive = right)
            y_value: Y-axis value (-1.0 to 1.0, negative = down, positive = up)
            duration: How long to hold the position in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Gamepad handler not available")
            return False
            
        try:
            # Clamp values to valid range
            x_value = max(-1.0, min(1.0, x_value))
            y_value = max(-1.0, min(1.0, y_value))
            
            if stick.lower() == 'left':
                self._virtual_gamepad.left_joystick_float(x_value_float=x_value, y_value_float=y_value)
            elif stick.lower() == 'right':
                self._virtual_gamepad.right_joystick_float(x_value_float=x_value, y_value_float=y_value)
            else:
                self._logger.error(f"Invalid stick: {stick}")
                return False
                
            self._virtual_gamepad.update()
            
            # Hold the position for the specified duration
            time.sleep(duration)
            
            # Return stick to center
            if stick.lower() == 'left':
                self._virtual_gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            else:
                self._virtual_gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                
            self._virtual_gamepad.update()
            
            self._logger.debug(f"Moved {stick} stick to ({x_value:.2f}, {y_value:.2f}) for {duration}s")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to move gamepad stick: {e}")
            return False
    
    def press_button(self, button: str, duration: float = 0.1) -> bool:
        """
        Press a gamepad button for specified duration.
        
        Args:
            button: Button to press (e.g., 'a', 'b', 'x', 'y', 'start', 'select')
            duration: How long to hold the button in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Gamepad handler not available")
            return False
            
        # Map button names to vgamepad constants
        button_map = {
            'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            'y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            'select': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            'back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            'lb': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            'rb': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            'left_shoulder': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            'right_shoulder': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
        }
        
        button_constant = button_map.get(button.lower())
        if button_constant is None:
            self._logger.error(f"Invalid button: {button}")
            return False
            
        try:
            # Press button
            self._virtual_gamepad.press_button(button=button_constant)
            self._virtual_gamepad.update()
            
            # Hold for duration
            time.sleep(duration)
            
            # Release button
            self._virtual_gamepad.release_button(button=button_constant)
            self._virtual_gamepad.update()
            
            self._logger.debug(f"Pressed {button} button for {duration}s")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to press gamepad button: {e}")
            return False
    
    def press_trigger(self, trigger: str, value: float, duration: float = 0.1) -> bool:
        """
        Press a gamepad trigger with specified intensity.
        
        Args:
            trigger: Trigger to press ('left', 'right')
            value: Trigger value (0.0 to 1.0)
            duration: How long to hold the trigger in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Gamepad handler not available")
            return False
            
        try:
            # Clamp value to valid range
            value = max(0.0, min(1.0, value))
            
            if trigger.lower() == 'left':
                self._virtual_gamepad.left_trigger_float(value_float=value)
            elif trigger.lower() == 'right':
                self._virtual_gamepad.right_trigger_float(value_float=value)
            else:
                self._logger.error(f"Invalid trigger: {trigger}")
                return False
                
            self._virtual_gamepad.update()
            
            # Hold for duration
            time.sleep(duration)
            
            # Release trigger
            if trigger.lower() == 'left':
                self._virtual_gamepad.left_trigger_float(value_float=0.0)
            else:
                self._virtual_gamepad.right_trigger_float(value_float=0.0)
                
            self._virtual_gamepad.update()
            
            self._logger.debug(f"Pressed {trigger} trigger to {value:.2f} for {duration}s")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to press gamepad trigger: {e}")
            return False
    
    def press_dpad(self, direction: str, duration: float = 0.1) -> bool:
        """
        Press a directional pad direction.
        
        Args:
            direction: Direction to press ('up', 'down', 'left', 'right')
            duration: How long to hold the direction in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Gamepad handler not available")
            return False
            
        # Map direction names to vgamepad constants
        dpad_map = {
            'up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            'down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            'left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            'right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
        }
        
        dpad_constant = dpad_map.get(direction.lower())
        if dpad_constant is None:
            self._logger.error(f"Invalid D-pad direction: {direction}")
            return False
            
        try:
            # Press D-pad direction
            self._virtual_gamepad.press_button(button=dpad_constant)
            self._virtual_gamepad.update()
            
            # Hold for duration
            time.sleep(duration)
            
            # Release D-pad direction
            self._virtual_gamepad.release_button(button=dpad_constant)
            self._virtual_gamepad.update()
            
            self._logger.debug(f"Pressed D-pad {direction} for {duration}s")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to press D-pad: {e}")
            return False
    
    def release_all(self) -> bool:
        """
        Release all buttons, sticks, and triggers (return to neutral state).
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            self._logger.error("Gamepad handler not available")
            return False
            
        try:
            # Reset all sticks to center
            self._virtual_gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            self._virtual_gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
            
            # Reset all triggers
            self._virtual_gamepad.left_trigger_float(value_float=0.0)
            self._virtual_gamepad.right_trigger_float(value_float=0.0)
            
            # Release all buttons (this automatically releases all pressed buttons)
            self._virtual_gamepad.reset()
            
            self._virtual_gamepad.update()
            
            self._logger.debug("Released all gamepad controls")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to release gamepad controls: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if the gamepad handler is available and properly initialized.
        
        Returns:
            True if the handler is available and can be used, False otherwise
        """
        return VGAMEPAD_AVAILABLE and self._initialized and self._virtual_gamepad is not None
    
    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.
        
        Returns:
            Platform name as a string
        """
        return "Windows"