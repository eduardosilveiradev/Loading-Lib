"""ASCII art loading screens for PyLoading."""
import sys
import time
from typing import List, Optional
from .base import BaseLoader

class ASCIILoader(BaseLoader):
    """Loading screen with ASCII art animations."""

    # Pre-defined ASCII art patterns
    PATTERNS = {
        'rocket': [
            """
      |
      |
     /_\\
    |=+=|
     |_|
    /| |\\
   //| |\\\\
  // | | \\\\
 //  |_|  \\\\
||   | |   ||
||   | |   ||
||   |_|   ||
||  /| |\\  ||
|| //| |\\\\ ||
||// |_| \\\\||
|//  | |  \\\\|
//   |_|   \\\\
""",
            """
         |
         |
        /_\\
       |=+=|
        |_|
       /| |\\
      //| |\\\\
     // | | \\\\
    //  |_|  \\\\
   ||   | |   ||
   ||   | |   ||
   ||   |_|   ||
   ||  /| |\\  ||
   || //| |\\\\ ||
   ||// |_| \\\\||
   |//  | |  \\\\|
   //   |_|   \\\\
""",
            """
            |
            |
           /_\\
          |=+=|
           |_|
          /| |\\
         //| |\\\\
        // | | \\\\
       //  |_|  \\\\
      ||   | |   ||
      ||   | |   ||
      ||   |_|   ||
      ||  /| |\\  ||
      || //| |\\\\ ||
      ||// |_| \\\\||
      |//  | |  \\\\|
      //   |_|   \\\\
""",
        ],
        'clock': [
            """
     .--.
    /  . \\
   |   .  |
    \\  . /
     '--'
""",
            """
     .--.
    /  | \\
   |   .  |
    \\  . /
     '--'
""",
            """
     .--.
    /  . \\
   |   |  |
    \\  . /
     '--'
""",
            """
     .--.
    /  . \\
   |   .  |
    \\  | /
     '--'
""",
        ],
        'spinner': [
            """
     *
    ***
   *****
  *******
 *********
  *******
   *****
    ***
     *
""",
            """
     +
    +++
   +++++
  +++++++
 +++++++++
  +++++++
   +++++
    +++
     +
""",
            """
     o
    ooo
   ooooo
  ooooooo
 ooooooooo
  ooooooo
   ooooo
    ooo
     o
""",
        ],
        'wave': [
            """
  _____     _____ 
 /     \\   /     \\
/       \\_/       \\
""",
            """
      _____     _____
     /     \\   /     \\
____/       \\_/       \\
""",
            """
           _____     _____
          /     \\   /     \\
_________/       \\_/       \\
"""
        ],
        'bounce': [
            """
   ( ●    )

_________________
""",
            """
      ( ●    )

_________________
""",
            """

         ( ●    )

_________________
""",
            """

    ( ●    )
_________________
"""
        ],
        'radar': [
            """
    ╭───────╮
    │ ╲     │
    │   ╲   │
    │     ╲ │
    ╰───────╯
""",
            """
    ╭───────╮
    │     ╱ │
    │   ╱   │
    │ ╱     │
    ╰───────╯
""",
            """
    ╭───────╮
    │ ╱     │
    │   ╱   │
    │     ╱ │
    ╰───────╯
""",
            """
    ╭───────╮
    │     ╲ │
    │   ╲   │
    │ ╲     │
    ╰───────╯
"""
        ]
    }

    def __init__(self, pattern: str = 'rocket', speed: float = 0.2):
        """
        Initialize ASCII art loader.

        Args:
            pattern: Name of the ASCII art pattern ('rocket', 'clock', 'spinner', 'wave', 'bounce', 'radar')
            speed: Animation speed in seconds
        """
        super().__init__()
        self._frames = self.PATTERNS.get(pattern, self.PATTERNS['rocket'])
        self._speed = speed
        self._frame_height = max(len(frame.split('\n')) for frame in self._frames)

    def _animate(self):
        """Animate the ASCII art."""
        idx = 0
        while not self._stop_event.is_set():
            with self._lock:
                # Clear entire frame area
                if idx > 0:
                    # Move up by frame height + 1 for message line
                    self._move_cursor_up(self._frame_height + 1)

                # Clear all lines in frame area
                for _ in range(self._frame_height + 1):
                    self._clear_line()
                    sys.stdout.write('\n')

                # Move back up to start drawing
                self._move_cursor_up(self._frame_height + 1)

                # Display current frame with message
                frame = self._frames[idx].rstrip()  # Remove trailing whitespace
                message_lines = [
                    frame,
                    f"\n{self._message}" if self._message else ""
                ]
                sys.stdout.write('\n'.join(message_lines))
                sys.stdout.flush()

            idx = (idx + 1) % len(self._frames)
            time.sleep(self._speed)