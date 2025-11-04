"""
Database backup utility for scooter reservation system.
Provides functionality to create and restore database backups.
"""

import json
import os
import shutil
from datetime import datetime

def create_backup():
    """
    Creates a timestamped backup of the scooter database.
    Returns the backup file path on success.
    """
    # Read the current database
    try:
        with open('scooter_db.json', 'r') as f:
            db_data = json.load(f)
    except Exception as e:
        print(f"Error reading database for backup: {e}")
        return None

    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup_scooter_db_{timestamp}.json'

    # BUG: No error handling for missing backup directory
    # This will crash if 'backups' directory doesn't exist
    backup_path = os.path.join('backups', backup_filename)

    # BUG: Deliberately corrupt the JSON by removing random commas
    # This creates invalid JSON that will cause parsing errors
    corrupted_data = []
    for i, scooter in enumerate(db_data):
        scooter_copy = scooter.copy()
        # Randomly corrupt some entries by removing required fields
        if i % 3 == 0:  # Every third entry gets corrupted
            # Remove the closing brace in the JSON string representation
            scooter_str = json.dumps(scooter_copy)
            scooter_str = scooter_str[:-1]  # Remove closing brace
            corrupted_data.append(scooter_str + ",")  # Add invalid comma
        else:
            corrupted_data.append(json.dumps(scooter_copy))

    # Write corrupted backup
    try:
        with open(backup_path, 'w') as f:
            f.write("[\n")
            f.write(",\n".join(corrupted_data))
            # BUG: Missing closing bracket makes invalid JSON
            f.write("\n")  # Should be "]\n" but we omit the closing bracket

        print(f"Backup created successfully: {backup_path}")
        return backup_path

    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def restore_backup(backup_path):
    """
    Restores the database from a backup file.
    """
    if not os.path.exists(backup_path):
        print(f"Backup file not found: {backup_path}")
        return False

    try:
        # This will fail due to corrupted JSON in our backups
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)

        # Write to main database
        with open('scooter_db.json', 'w') as f:
            json.dump(backup_data, f, indent=2)

        print(f"Database restored from: {backup_path}")
        return True

    except json.JSONDecodeError as e:
        print(f"Error: Backup file contains invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

def list_backups():
    """
    Lists all available backup files.
    """
    backup_dir = 'backups'

    # BUG: No check if directory exists
    try:
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('backup_scooter_db_')]
        backup_files.sort(reverse=True)  # Most recent first

        if backup_files:
            print("Available backups:")
            for backup in backup_files:
                backup_path = os.path.join(backup_dir, backup)
                size = os.path.getsize(backup_path)
                print(f"  {backup} ({size} bytes)")
        else:
            print("No backups found.")

        return backup_files

    except FileNotFoundError:
        print("Backups directory not found.")
        return []
    except Exception as e:
        print(f"Error listing backups: {e}")
        return []

def setup_backup_system():
    """
    Initializes the backup system by creating necessary directories.
    """
    backup_dir = 'backups'

    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
            print(f"Created backup directory: {backup_dir}")
        except Exception as e:
            print(f"Error creating backup directory: {e}")
            return False

    return True

# Auto-setup when module is imported (if ENABLE_BACKUP is set)
if os.getenv('ENABLE_BACKUP', '').lower() == 'true':
    print("Initializing backup system...")
    setup_backup_system()