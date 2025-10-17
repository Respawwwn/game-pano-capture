"""
Interface definition for gamepad handlers.

This module defines the contract that all platform-specific gamepad implementations must follow.
"""

from abc import ABC, abstractmethod


class IGamepadHandler(ABC):
    """
    Interface for platform-specific gamepad implementations.
    
    All gamepad handlers must implement this interface to ensure
    consistent behavior across different platforms.
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the gamepad handler.
        
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
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
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def press_button(self, button: str, duration: float = 0.1) -> bool:
        """
        Press a gamepad button for specified duration.
        
        Args:
            button: Button to press (e.g., 'a', 'b', 'x', 'y', 'start', 'select')
            duration: How long to hold the button in seconds
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def press_trigger(self, trigger: str, value: float, duration: float = 0.1) -> bool:
        """
        Press a gamepad trigger with specified intensity.
        
        Args:
            trigger: Trigger to press ('left', 'right')
            value: Trigger value (0.0 to 1.0)
            duration: How long to hold the trigger in seconds
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def press_dpad(self, direction: str, duration: float = 0.1) -> bool:
        """
        Press a directional pad direction.
        
        Args:
            direction: Direction to press ('up', 'down', 'left', 'right')
            duration: How long to hold the direction in seconds
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def release_all(self) -> bool:
        """
        Release all buttons, sticks, and triggers (return to neutral state).
        
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the gamepad handler is available and properly initialized.
        
        Returns:
            True if the handler is available and can be used, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """
        Get the name of the platform this handler is designed for.
        
        Returns:
            Platform name as a string (e.g., 'macOS', 'Windows', 'Linux')
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass