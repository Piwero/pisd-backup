import datetime
import os

from src.utils.logger import info_log, warning_log
from src.utils.manage_backups import MAX_BACKUPS, manage_backups


def backup_raspberry_pi():
    info_log("Backing up Raspberry Pi...")

    # Set a default value for max_backups
    max_backups = MAX_BACKUPS

    # Set the backup filename based on the hostname, current date, hour, and minute
    bk_filename = f"{os.uname().nodename}.{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.img"
    backup_path = f"/home/{os.getlogin()}/backup-raspis/{bk_filename}"

    # Create a backup of the Raspberry Pi using dd
    exit_code = os.system(f"sudo mount -a && sudo dd bs=4M if=/dev/mmcblk0 of={backup_path}")

    if exit_code == 0:
        info_log(f"Created backup: {backup_path}")
        manage_backups(os.uname().nodename, max_backups)
    else:
        warning_log("Failed to create backup.")

    # Run pishrink.sh on the created backup
    exit_code = os.system(f"sudo pishrink.sh {backup_path}")

    if exit_code == 0:
        info_log("Ran pishrink.sh on the backup.")
    else:
        warning_log("Failed to run pishrink.sh.")
