import sys
import time
from typing import List, Tuple, Optional
from .base import BaseLoader
from .color_selector import ColorSelector
from .config import Config

class Spinner(BaseLoader):
    """Animated spinner with customizable characters and colors."""

    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'pulse':
        ['█', '▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
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

    @classmethod
    def select_color(cls) -> str:
        """
        Open an interactive color selector.

        Returns:
            str: The name of the selected color
        """
        selector = ColorSelector()
        return selector.get_color()

    def __init__(self,
                 style: Optional[str] = None,
                 color: Optional[str] = None,
                 speed: Optional[float] = None,
                 interactive_color: bool = False,
                 config_path: Optional[str] = None):
        """
        Initialize the spinner.

        Args:
            style: The spinner style ('dots', 'line', 'arrow', 'pulse')
            color: The spinner color ('red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')
            speed: Animation speed in seconds
            interactive_color: If True, opens color selector on initialization
            config_path: Optional path to configuration file
        """
        super().__init__()

        # Load config
        self._config = Config(config_path)
        config = self._config.get_spinner_config()

        # Use provided values or fall back to config
        if interactive_color:
            color = self.select_color()
            self._config.update_spinner_config(color=color)

        self._frames = self.SPINNERS.get(style or config['style'], self.SPINNERS['dots'])
        self._color = self.COLORS.get(color or config['color'], self.COLORS['white'])
        self._speed = speed or config['speed']

    def save_preferences(self):
        """Save current spinner preferences to config file."""
        style = next((k for k, v in self.SPINNERS.items() if v == self._frames), 'dots')
        color = next((k for k, v in self.COLORS.items() if v == self._color), 'white')

        self._config.update_spinner_config(
            style=style,
            color=color,
            speed=self._speed
        )

    def _animate(self):
        """Animate the spinner."""
        idx = 0
        while not self._stop_event.is_set():
            with self._lock:
                self._clear_line()
                frame = self._frames[idx]
                sys.stdout.write(
                    f"{self._color}{frame} {self._message}{self.COLORS['reset']}"
                )
                sys.stdout.flush()

            idx = (idx + 1) % len(self._frames)
            time.sleep(self._speed)