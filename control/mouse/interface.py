"""
Interface definition for mouse handlers.

This module defines the contract that all platform-specific mouse implementations must follow.
"""

from abc import ABC, abstractmethod


class IMouseHandler(ABC):
    """
    Interface for platform-specific mouse implementations.
    
    All mouse handlers must implement this interface to ensure
    consistent behavior across different platforms.
    """
    
    @abstractmethod
    def move_relative(self, dx: int, dy: int) -> bool:
        """
        Move the mouse cursor by relative amounts.
        
        Args:
            dx: Horizontal movement in pixels (positive = right, negative = left)
            dy: Vertical movement in pixels (positive = down, negative = up)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def move_absolute(self, x: int, y: int) -> bool:
        """
        Move the mouse cursor to absolute screen coordinates.
        
        Args:
            x: Horizontal position in pixels
            y: Vertical position in pixels
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        """
        Get the current mouse cursor position.
        
        Returns:
            Tuple of (x, y) coordinates in pixels
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def click(self, button: str = "left") -> bool:
        """
        Click a mouse button.
        
        Args:
            button: Mouse button to click ('left', 'right', 'middle')
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def scroll(self, dx: int = 0, dy: int = 0) -> bool:
        """
        Scroll the mouse wheel.
        
        Args:
            dx: Horizontal scroll amount (positive = right, negative = left)
            dy: Vertical scroll amount (positive = up, negative = down)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            NotImplementedError: If the method is not implemented
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the mouse handler is available and properly initialized.
        
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