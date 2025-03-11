import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import random
from pyloading import Spinner, ProgressBar, ASCIILoader

def demo_interactive_color():
    """Demonstrate interactive color selection."""
    print("\nInteractive Color Selection Demo:")
    print("Select a color for your spinner:")
    spinner = Spinner(style='dots', interactive_color=True)
    spinner.start("Testing interactive color selection")
    time.sleep(3)
    spinner.stop()

    # Save the selected color preference
    spinner.save_preferences()
    print("\nColor preference saved! Next time you create a spinner, it will use this color by default.")

def demo_persistent_config():
    """Demonstrate loading from saved configuration."""
    print("\nPersistent Configuration Demo:")
    print("Creating spinner with saved preferences...")
    spinner = Spinner()  # Will use saved preferences
    spinner.start("Using saved preferences")
    time.sleep(3)
    spinner.stop()

def demo_spinner():
    """Demonstrate different spinner styles."""
    print("\nSpinner Styles Demo:")
    styles = ['dots', 'line', 'arrow', 'pulse']
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan']

    for style in styles:
        for color in colors:
            spinner = Spinner(style=style, color=color)
            spinner.start(f"Testing {style} style in {color}")
            time.sleep(2)
            spinner.stop()

def demo_progress_bar():
    """Demonstrate progress bar functionality."""
    print("\nProgress Bar Demo:")
    total = 100
    progress = ProgressBar(total, color='green')
    progress.start("Processing items...")

    for i in range(total + 1):
        progress.update(i)
        time.sleep(0.1)  # Simulate work
    progress.stop()

def demo_progress_bar_styles():
    """Demonstrate different progress bar styles."""
    print("\nProgress Bar Styles Demo:")
    styles = [
        ('█', '░', 'blue'),
        ('▓', '▒', 'red'),
        ('>', '-', 'yellow'),
        ('=', ' ', 'purple')
    ]

    for fill_char, empty_char, color in styles:
        progress = ProgressBar(50, fill_char=fill_char, empty_char=empty_char, color=color)
        progress.start(f"Style: {fill_char}{empty_char}")

        for i in range(51):
            progress.update(i)
            time.sleep(0.05)
        progress.stop()

def demo_ascii_art():
    """Demonstrate ASCII art loading screens."""
    print("\nASCII Art Loading Screens Demo:")

    # Demonstrate rocket animation
    print("\nRocket Launch Sequence:")
    rocket = ASCIILoader(pattern='rocket', speed=0.3)
    rocket.start("Initiating launch sequence...")
    time.sleep(3)
    rocket.stop()

    # Demonstrate clock animation
    print("\nClock Animation:")
    clock = ASCIILoader(pattern='clock', speed=0.2)
    clock.start("Time is ticking...")
    time.sleep(3)
    clock.stop()

    # Demonstrate spinner animation
    print("\nSpinner Animation:")
    spinner = ASCIILoader(pattern='spinner', speed=0.2)
    spinner.start("Processing with style...")
    time.sleep(3)
    spinner.stop()

    # Demonstrate wave animation
    print("\nWave Animation:")
    wave = ASCIILoader(pattern='wave', speed=0.2)
    wave.start("Making waves...")
    time.sleep(3)
    wave.stop()

    # Demonstrate bounce animation
    print("\nBounce Animation:")
    bounce = ASCIILoader(pattern='bounce', speed=0.15)
    bounce.start("Bouncing ball effect...")
    time.sleep(3)
    bounce.stop()

    # Demonstrate radar animation
    print("\nRadar Scanner:")
    radar = ASCIILoader(pattern='radar', speed=0.2)
    radar.start("Scanning for signals...")
    time.sleep(3)
    radar.stop()

if __name__ == "__main__":
    demo_interactive_color()
    demo_persistent_config()  # Show that preferences were saved
    demo_spinner()
    demo_progress_bar()
    demo_progress_bar_styles()
    demo_ascii_art()  # Added ASCII art demo