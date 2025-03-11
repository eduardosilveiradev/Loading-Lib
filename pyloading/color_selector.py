import sys
import os
from typing import List, Tuple
from .base import BaseLoader


class ColorSelector:
    """Interactive color palette selector for terminal."""

    def __init__(self):
        self._colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
        }
        self._reset = "\033[0m"
        self._current_index = 0

    def _get_char(self) -> str:
        """Get a single character from stdin."""
        if os.name == "nt":  # Windows
            import msvcrt

            return msvcrt.getch().decode("utf-8", errors="ignore")
        else:  # Unix-like
            import tty
            import termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def _display_colors(self):
        """Display all available colors with selection indicator."""
        os.system("cls" if os.name == "nt" else "clear")  # Clear screen
        print("Select a color for your preferred style:")
        print("Use ↑/↓ arrows to navigate, Enter to select, q to quit\n")

        for i, (name, code) in enumerate(self._colors.items()):
            indicator = "→ " if i == self._current_index else "  "
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

            if os.name == "nt":  # Windows
                import msvcrt

                key = msvcrt.getch()

                if key in (b"\xe0", b"\x00"):  # Special keys
                    key2 = msvcrt.getch()
                    if key2 == b"H":  # Up arrow
                        self._current_index = (self._current_index - 1) % len(
                            self._colors
                        )
                    elif key2 == b"P":  # Down arrow
                        self._current_index = (self._current_index + 1) % len(
                            self._colors
                        )
                elif key == b"\r":  # Enter
                    return color_names[self._current_index]
                elif key == b"q" or key == b"Q":  # Quit
                    return "white"
            else:  # Unix-like
                key = self._get_char()

                if key == "\x1b":  # Escape sequence for Unix
                    next_two = sys.stdin.read(2)
                    if next_two == "[A":  # Up arrow
                        self._current_index = (self._current_index - 1) % len(
                            self._colors
                        )
                    elif next_two == "[B":  # Down arrow
                        self._current_index = (self._current_index + 1) % len(
                            self._colors
                        )
                elif key == "\r" or key == "\n":  # Enter
                    return color_names[self._current_index]
                elif key.lower() == "q":  # Quit
                    return "white"  # Default color
