import sys
import termios
import tty
from typing import List, Tuple
from .base import BaseLoader

class ColorSelector:
    """Interactive color palette selector for terminal."""
    
    def __init__(self):
        self._colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
        }
        self._reset = '\033[0m'
        self._current_index = 0
        
    def _get_char(self) -> str:
        """Get a single character from stdin."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
    def _display_colors(self):
        """Display all available colors with selection indicator."""
        sys.stdout.write('\033[2J\033[H')  # Clear screen and move to top
        print("Use ↑/↓ arrows to navigate, Enter to select, q to quit\n")
        
        for i, (name, code) in enumerate(self._colors.items()):
            indicator = '→ ' if i == self._current_index else '  '
            print(f"{indicator}{code}Sample Text - {name}{self._reset}")
            
    def get_color(self) -> str:
        """
        Start the interactive color selection process.
        
        Returns:
            str: The name of the selected color
        """
        color_names = list(self._colors.keys())
        
        while True:
            self._display_colors()
            key = self._get_char()
            
            if key == '\x1b':  # Escape sequence
                next_two = sys.stdin.read(2)
                if next_two == '[A':  # Up arrow
                    self._current_index = (self._current_index - 1) % len(self._colors)
                elif next_two == '[B':  # Down arrow
                    self._current_index = (self._current_index + 1) % len(self._colors)
            elif key == '\r':  # Enter
                return color_names[self._current_index]
            elif key.lower() == 'q':  # Quit
                return 'white'  # Default color
