import datetime
import os
import sys

from crontab import CronTab

from src.utils.install_dependencies import install_dependencies
from src.utils.logger import info_log, warning_log

MAX_BACKUPS = 2  # Default value, can be adjusted


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


def setup_cronjob(cron_schedule):
    info_log("Setting up cronjob for option 2...")

    # Get the current user's username
    username = os.getlogin()

    # Get the path to the script
    script_path = os.path.abspath(__file__)

    # Add the cron job for option 2 with output redirection
    cron_command = f"sudo mount -a && sudo python3 {script_path} backup_raspberry_pi && sudo python3 {script_path} manage_backups"

    # Use a specific log file path or /dev/null if you don't need the output
    # Replace /path/to/logfile with the desired log file path

    # Create a new cron tab
    cron = CronTab(user=username)

    # Add the cron job for option 2
    job = cron.new(command=cron_command, comment="Backup Raspberry Pi")
    job.setall(cron_schedule)

    cron.write()

    info_log(f"Cronjob added. Schedule: {cron_schedule}")


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


def setup_nas_mount():
    info_log("Setting up NAS mount volume...")

    # Get NAS details from user
    nas_username = input("Enter NAS backup username: ")
    nas_password = input("Enter NAS backup password: ")
    nas_ip = input("Enter NAS IP: ")

    creds_path = "/etc/nas-backup-creds"
    backup_mount_path = f"/home/{os.getlogin()}/backup-raspis"
    fstab_entry = f"//{nas_ip}/backup-raspis {backup_mount_path} cifs credentials={creds_path},uid=1001 0 0"

    # Write credentials file
    try:
        with open(creds_path, "w") as creds_file:
            creds_file.write(f"username={nas_username}\npassword={nas_password}\n")
        os.system(f"sudo chmod 600 {creds_path}")
        info_log(f"NAS credentials saved at {creds_path}.")
    except Exception as e:
        warning_log(f"Failed to write NAS credentials: {e}")
        return

    # Create mount directory
    os.system(f"mkdir -p {backup_mount_path}")

    # Add to /etc/fstab
    try:
        with open("/etc/fstab", "a") as fstab:
            fstab.write(f"{fstab_entry}\n")
        info_log("NAS mount entry added to /etc/fstab.")
    except Exception as e:
        warning_log(f"Failed to update /etc/fstab: {e}")
        return

    # Mount all volumes
    exit_code = os.system("sudo mount -a")
    if exit_code == 0:
        info_log(f"NAS volume mounted successfully at {backup_mount_path}.")
        print(
            "\nFor DietPi users, use `sudo dietpi-config`, select option `9` and `14` (Autostart Options > custom script), and add `sudo mount -a` to ensure the NAS volume is mounted on startup.")
        print(
            "It is also recommended that after mounting the NAS, to run `sudo dietpi-drive_manager` and use the resize option.")
    else:
        warning_log("Failed to mount NAS volume. Please check /etc/fstab entries and retry.")


def main():
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "install_dependencies":
            install_dependencies()
        elif action == "backup_raspberry_pi":
            backup_raspberry_pi()
        elif action == "setup_cronjob":
            cron_schedule = input("Enter the custom cron schedule (e.g., '0 2 * * *'): ")
            setup_cronjob(cron_schedule)
        elif action == "manage_backups":
            manage_backups_input = sys.argv[2] if len(sys.argv) > 2 else None
            try:
                manage_backups_max = int(manage_backups_input) if manage_backups_input is not None else MAX_BACKUPS
            except ValueError:
                warning_log("Invalid input for maximum backups. Using default value.")
                manage_backups_max = MAX_BACKUPS
            manage_backups(os.uname().nodename, manage_backups_max)
        elif action == "setup_nas_mount":
            setup_nas_mount()
        elif action == "0":
            return
        else:
            print("Invalid action. Please provide a valid action.")
            return
    else:
        while True:
            print("Choose an option:")
            print("1. Install dependencies")
            print("2. Backup Raspberry Pi")
            print("3. Setup cronjob for option 2")
            print("4. Manage number of backups")
            print("5. Setup NAS mount volume")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                install_dependencies()
            elif choice == "2":
                backup_raspberry_pi()
            elif choice == "3":
                cron_schedule = input("Enter the custom cron schedule (e.g., '0 2 * * *'): ")
                setup_cronjob(cron_schedule)
            elif choice == "4":
                manage_backups_input = input("Enter the number of backups to keep: ")
                try:
                    manage_backups_max = int(manage_backups_input)
                except ValueError:
                    warning_log("Invalid input for maximum backups. Using default value.")
                    manage_backups_max = MAX_BACKUPS
                manage_backups(os.uname().nodename, manage_backups_max)
            elif choice == "5":
                setup_nas_mount()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
