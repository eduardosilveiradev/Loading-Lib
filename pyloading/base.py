import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Optional

class BaseLoader(ABC):
    """Base class for all loading indicators."""

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._message = ""

    def start(self, message: str = ""):
        """Start the loading animation."""
        if self._thread is not None and self._thread.is_alive():
            return

        self._message = message
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._animate)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """Stop the loading animation."""
        if self._thread is None:
            return

        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join()
        self._clear_line()
        sys.stdout.flush()

    def _clear_line(self):
        """Clear the current terminal line using ANSI escape sequences."""
        # \033[2K - Clear entire line
        # \033[G - Move cursor to beginning of line
        sys.stdout.write('\033[2K\033[G')
        sys.stdout.flush()

    def _move_cursor_up(self, lines: int = 1):
        """Move cursor up by specified number of lines."""
        sys.stdout.write(f'\033[{lines}A')
        sys.stdout.flush()

    def _move_cursor_down(self, lines: int = 1):
        """Move cursor down by specified number of lines."""
        sys.stdout.write(f'\033[{lines}B')
        sys.stdout.flush()

    @abstractmethod
    def _animate(self):
        """Abstract method for animation implementation."""
        pass

    def update_message(self, message: str):
        """Update the loading message."""
        with self._lock:
            self._message = message