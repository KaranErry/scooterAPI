"""
Unit tests for configuration management.
Tests configuration loading, parsing, and fallback behavior.
"""

import unittest
import json
import os
import tempfile
import shutil
import config_loader


class TestConfigurationManagement(unittest.TestCase):
    """Test configuration loading and management."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_default_configuration_loading(self):
        """Test loading default configuration when no file exists."""
        loader = config_loader.ConfigLoader("nonexistent_config.json")
        config = loader.load_config()

        self.assertIsNotNone(config)
        self.assertIn('app', config)
        self.assertEqual(config['app']['port'], 8080)

    def test_config_file_parsing(self):
        """Test parsing of valid configuration file."""
        # Create a valid config file
        test_config = {
            "app": {
                "port": 9999,
                "debug": True,
                "host": "0.0.0.0"
            },
            "database": {
                "file": "custom_db.json"
            }
        }

        with open('test_config.json', 'w') as f:
            json.dump(test_config, f)

        loader = config_loader.ConfigLoader("test_config.json")
        config = loader.load_config()

        # This test will fail due to the silent failure bug
        self.assertEqual(config['app']['port'], 9999, "Should load custom port from file")
        self.assertTrue(config['app']['debug'], "Should load debug setting from file")

    def test_malformed_config_fallback(self):
        """Test fallback behavior with malformed configuration file."""
        # Create invalid JSON config
        with open('bad_config.json', 'w') as f:
            f.write('{"app": {"port": 9999,}}')  # Invalid JSON (trailing comma)

        loader = config_loader.ConfigLoader("bad_config.json")
        config = loader.load_config()

        # Should fall back to defaults
        self.assertEqual(config['app']['port'], 8080)
        self.assertFalse(config['app']['debug'])

    def test_config_key_access(self):
        """Test configuration key access using dot notation."""
        loader = config_loader.ConfigLoader()
        loader.load_config()

        # Test getting nested configuration values
        port = loader.get('app.port')
        self.assertEqual(port, 8080)

        debug = loader.get('app.debug')
        self.assertFalse(debug)

        # Test getting non-existent keys with defaults
        custom_value = loader.get('app.custom_setting', 'default_value')
        self.assertEqual(custom_value, 'default_value')

    def test_config_sections_retrieval(self):
        """Test retrieval of configuration sections."""
        loader = config_loader.ConfigLoader()
        loader.load_config()

        app_config = loader.get_app_config()
        self.assertIn('port', app_config)
        self.assertIn('debug', app_config)

        db_config = loader.get_database_config()
        self.assertIn('file', db_config)

        payment_config = loader.get_payment_config()
        self.assertIn('currency', payment_config)

    def test_config_reload(self):
        """Test configuration reloading functionality."""
        # Create initial config
        initial_config = {"app": {"port": 8080}}
        with open('reload_test.json', 'w') as f:
            json.dump(initial_config, f)

        loader = config_loader.ConfigLoader("reload_test.json")
        config = loader.load_config()

        # Modify config file
        updated_config = {"app": {"port": 9000}}
        with open('reload_test.json', 'w') as f:
            json.dump(updated_config, f)

        # Reload configuration
        reloaded_config = loader.reload_config()

        # This might fail due to the silent failure bug
        self.assertEqual(reloaded_config['app']['port'], 9000, "Config should be reloaded with new values")


if __name__ == '__main__':
    unittest.main()