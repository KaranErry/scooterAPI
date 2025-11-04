"""
Unit tests for database backup functionality.
Tests the backup and restore capabilities of the scooter database.
"""

import unittest
import json
import os
import tempfile
import shutil
import db_backup


class TestDatabaseBackup(unittest.TestCase):
    """Test database backup and restore functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create a test database
        self.test_data = [
            {"id": "1", "lat": 10.0, "lng": 20.0, "is_reserved": False},
            {"id": "2", "lat": 15.0, "lng": 25.0, "is_reserved": True}
        ]
        with open('scooter_db.json', 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_backup_system_initialization(self):
        """Test that backup system initializes properly."""
        result = db_backup.setup_backup_system()

        self.assertTrue(result)
        self.assertTrue(os.path.exists('backups'))

    def test_backup_creation(self):
        """Test backup creation functionality."""
        # Setup backup directory first
        db_backup.setup_backup_system()

        # Create backup
        backup_path = db_backup.create_backup()

        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))

    def test_backup_restore_integrity(self):
        """Test that backup can be restored without data loss."""
        # Setup backup directory
        db_backup.setup_backup_system()

        # Create backup
        backup_path = db_backup.create_backup()
        self.assertIsNotNone(backup_path)

        # Attempt to restore - this test will fail due to JSON corruption bug
        success = db_backup.restore_backup(backup_path)

        # This assertion should pass, but will fail due to corrupted JSON
        self.assertTrue(success, "Backup restore should succeed with valid data")

    def test_list_available_backups(self):
        """Test listing of available backup files."""
        # Setup and create a backup
        db_backup.setup_backup_system()
        db_backup.create_backup()

        backups = db_backup.list_backups()

        self.assertIsInstance(backups, list)
        self.assertGreater(len(backups), 0)


if __name__ == '__main__':
    unittest.main()