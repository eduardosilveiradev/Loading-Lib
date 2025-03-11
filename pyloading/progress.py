import sys
import time
from typing import Optional
from .base import BaseLoader
from .spinner import Spinner  # Add import for Spinner class

class ProgressBar(BaseLoader):
    """Progress bar with ETA calculation and customizable appearance."""

    def __init__(self, total: int, width: int = 40, fill_char: str = '█',
                 empty_char: str = '░', color: str = 'blue'):
        """
        Initialize the progress bar.

        Args:
            total: Total number of items
            width: Width of the progress bar
            fill_char: Character for filled portion
            empty_char: Character for empty portion
            color: Progress bar color
        """
        super().__init__()
        self.total = total
        self.width = width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self._color = Spinner.COLORS.get(color, Spinner.COLORS['blue'])
        self._current = 0
        self._start_time: Optional[float] = None

    def update(self, current: int):
        """Update the progress bar."""
        with self._lock:
            self._current = min(current, self.total)
            if self._start_time is None:
                self._start_time = time.time()
            self._render()

    def _calculate_eta(self) -> str:
        """Calculate estimated time remaining."""
        if self._start_time is None or self._current == 0:
            return "??:??"

        elapsed = time.time() - self._start_time
        rate = self._current / elapsed
        remaining = (self.total - self._current) / rate if rate > 0 else 0

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def _render(self):
        """Render the progress bar."""
        percentage = (self._current / self.total) * 100
        filled_width = int(self.width * self._current // self.total)

        bar = (
            self.fill_char * filled_width +
            self.empty_char * (self.width - filled_width)
        )

        eta = self._calculate_eta()
        output = (
            f"\r{self._color}Progress: [{bar}] "
            f"{percentage:0.1f}% ({self._current}/{self.total}) "
            f"ETA: {eta} {self._message}{Spinner.COLORS['reset']}"
        )

        sys.stdout.write(output)
        sys.stdout.flush()

    def _animate(self):
        """Implementation of abstract method."""
        while not self._stop_event.is_set():
            with self._lock:
                self._render()
            time.sleep(0.1)