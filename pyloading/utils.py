import os
import sys
from typing import Callable

def supports_color() -> bool:
    """Check if the terminal supports colors."""
    if os.environ.get('FORCE_COLOR', '0') != '0':
        return True
        
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    return supported_platform and is_a_tty

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def with_spinner(spinner_cls: Callable, message: str = "Processing..."):
    """Decorator to add a spinner to a function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            spinner = spinner_cls()
            spinner.start(message)
            try:
                result = func(*args, **kwargs)
                spinner.stop()
                return result
            except Exception as e:
                spinner.stop()
                raise e
        return wrapper
    return decorator
