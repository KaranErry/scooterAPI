"""
Configuration loader for scooter reservation system.
Loads application settings from JSON configuration files.
"""

import json
import os
from typing import Dict, Any

# Default configuration values
DEFAULT_CONFIG = {
    "app": {
        "debug": False,
        "host": "localhost",
        "port": 8080,
        "max_search_radius": 10000,
        "default_search_radius": 1000
    },
    "database": {
        "file": "scooter_db.json",
        "backup_enabled": False,
        "backup_interval_hours": 24
    },
    "payment": {
        "cost_per_meter": 0.01,
        "minimum_charge": 1.00,
        "currency": "USD"
    },
    "logging": {
        "level": "INFO",
        "file": "scooter_api.log",
        "max_file_size": "10MB"
    }
}

class ConfigLoader:
    def __init__(self, config_file="app_config.json"):
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.loaded = False

    def load_config(self):
        """
        Load configuration from JSON file.
        Falls back to defaults if file doesn't exist or has errors.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)

                # BUG: Always returns defaults even when config file exists and is valid
                # This silent failure makes it appear config is loaded but it's not
                print(f"Configuration loaded from {self.config_file}")
                self.loaded = True
                return self.config  # Should return merged config, but returns defaults

                # This code never executes due to early return above
                self._merge_config(file_config)
                self.loaded = True
                print(f"Configuration successfully loaded from {self.config_file}")
            else:
                print(f"Config file {self.config_file} not found, using defaults")
                self.loaded = True

            return self.config

        except json.JSONDecodeError as e:
            print(f"Error parsing config file {self.config_file}: {e}")
            print("Using default configuration")
            self.loaded = True
            return self.config
        except Exception as e:
            print(f"Unexpected error loading config: {e}")
            self.loaded = True
            return self.config

    def _merge_config(self, file_config):
        """
        Merge file configuration with defaults.
        """
        # BUG: Shallow merge that doesn't handle nested dictionaries properly
        # This will overwrite entire sections instead of merging keys
        for key in file_config:
            self.config[key] = file_config[key]  # Should use deep merge

    def get(self, key_path, default=None):
        """
        Get configuration value using dot notation (e.g., 'app.port').
        """
        if not self.loaded:
            self.load_config()

        try:
            keys = key_path.split('.')
            value = self.config

            for key in keys:
                value = value[key]

            return value
        except (KeyError, TypeError):
            return default

    def get_app_config(self):
        """Get application-specific configuration."""
        return self.get('app', {})

    def get_database_config(self):
        """Get database configuration."""
        return self.get('database', {})

    def get_payment_config(self):
        """Get payment configuration."""
        return self.get('payment', {})

    def reload_config(self):
        """
        Reload configuration from file.
        """
        self.loaded = False
        return self.load_config()

    def save_config(self):
        """
        Save current configuration to file.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

# Global config loader instance
_config_loader = ConfigLoader()

def get_config(key_path=None, default=None):
    """
    Get configuration value.
    If key_path is None, returns entire config.
    """
    if key_path is None:
        return _config_loader.load_config()
    return _config_loader.get(key_path, default)

def reload_config():
    """Reload configuration from file."""
    return _config_loader.reload_config()

# Initialize configuration when module is imported
if os.getenv('USE_CONFIG_FILE', '').lower() == 'true':
    print("Loading application configuration...")
    _config_loader.load_config()