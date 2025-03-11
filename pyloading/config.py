"""Configuration management for PyLoading."""
import json
import os
from typing import Dict, Any, Optional

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.pyloading/config.json")
DEFAULT_CONFIG = {
    "spinner": {
        "style": "dots",
        "color": "white",
        "speed": 0.1
    },
    "progress_bar": {
        "color": "blue",
        "width": 40,
        "fill_char": "█",
        "empty_char": "░"
    }
}

class Config:
    """Handle loading and saving of user preferences."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._ensure_config_dir()
        self.config = self.load()
    
    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_spinner_config(self) -> Dict[str, Any]:
        """Get spinner configuration."""
        return self.config.get('spinner', DEFAULT_CONFIG['spinner'])
    
    def get_progress_bar_config(self) -> Dict[str, Any]:
        """Get progress bar configuration."""
        return self.config.get('progress_bar', DEFAULT_CONFIG['progress_bar'])
    
    def update_spinner_config(self, **kwargs):
        """Update spinner configuration."""
        if 'spinner' not in self.config:
            self.config['spinner'] = DEFAULT_CONFIG['spinner'].copy()
        self.config['spinner'].update(kwargs)
        self.save()
    
    def update_progress_bar_config(self, **kwargs):
        """Update progress bar configuration."""
        if 'progress_bar' not in self.config:
            self.config['progress_bar'] = DEFAULT_CONFIG['progress_bar'].copy()
        self.config['progress_bar'].update(kwargs)
        self.save()
