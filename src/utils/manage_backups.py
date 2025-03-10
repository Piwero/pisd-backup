import os

from utils.logger import info_log

MAX_BACKUPS = 2  # Default value, can be adjusted


def manage_backups(hostname, max_backups):
    backup_dir = f"/home/{os.getlogin()}/backup-raspis/"
    backups = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]

    # Filter backups for the current hostname
    host_backups = [f for f in backups if f.startswith(hostname)]

    # Sort backups by modification time (oldest first)
    host_backups.sort(key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)))

    # Keep only the latest max_backups backups
    if len(host_backups) > max_backups:
        backups_to_delete = host_backups[:-max_backups]

        for backup in backups_to_delete:
            backup_path = os.path.join(backup_dir, backup)
            os.remove(backup_path)
            info_log(f"Deleted old backup: {backup_path}")
