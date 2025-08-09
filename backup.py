# backup.py

import shutil
from datetime import datetime
import os

def create_backup(db_file='finance.db'):
    """
    Creates a timestamped backup of the database file.

    Args:
        db_file (str): The path to the database file to back up.
    """
    if not os.path.exists(db_file):
        print(f"❌ Error: Database file '{db_file}' not found.")
        return

    # Create a 'backups' directory if it doesn't exist
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate a filename with a precise timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"finance_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        # shutil.copyfile is perfect for copying a single file
        shutil.copyfile(db_file, backup_path)
        print(f"✅ Backup created successfully: {backup_path}")
    except Exception as e:
        print(f"❌ An error occurred while creating the backup: {e}")

# backup.py

def restore_from_backup():
    """
    Lists available backups and restores the database from a chosen file.
    """
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        print("❌ No backup directory found.")
        return

    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    if not backups:
        print("❌ No backup files found in the 'backups' directory.")
        return

    print("\n--- Available Backups ---")
    for i, filename in enumerate(backups, 1):
        print(f"{i}. {filename}")

    try:
        choice = int(input("\nEnter the number of the backup to restore (or 0 to cancel): "))
        if choice == 0:
            print("Restore cancelled.")
            return
        if not 1 <= choice <= len(backups):
            print("❌ Invalid choice.")
            return

        selected_backup = backups[choice - 1]
        backup_path = os.path.join(backup_dir, selected_backup)

        # --- CRUCIAL: Get user confirmation ---
        confirm = input(f"\n⚠️ WARNING: This will overwrite ALL current data with the contents of '{selected_backup}'.\nAre you sure you want to continue? (yes/no): ").lower()

        if confirm == 'yes':
            shutil.copyfile(backup_path, 'finance.db')
            print(f"✅ Database restored successfully from {selected_backup}.")
        else:
            print("Restore cancelled.")

    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        print(f"❌ An error occurred during restore: {e}")