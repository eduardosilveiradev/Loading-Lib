import sys
import time
from typing import List, Tuple
from .base import BaseLoader

class Spinner(BaseLoader):
    """Animated spinner with customizable characters and colors."""
    
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'pulse': ['█', '▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
    }
    
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    def __init__(self, style: str = 'dots', color: str = 'white', speed: float = 0.1):
        """
        Initialize the spinner.
        
        Args:
            style: The spinner style ('dots', 'line', 'arrow', 'pulse')
            color: The spinner color ('red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')
            speed: Animation speed in seconds
        """
        super().__init__()
        self._frames = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self._color = self.COLORS.get(color, self.COLORS['white'])
        self._speed = speed
        
    def _animate(self):
        """Animate the spinner."""
        idx = 0
        while not self._stop_event.is_set():
            with self._lock:
                self._clear_line()
                frame = self._frames[idx]
                sys.stdout.write(f"{self._color}{frame} {self._message}{self.COLORS['reset']}")
                sys.stdout.flush()
            
            idx = (idx + 1) % len(self._frames)
            time.sleep(self._speed)
