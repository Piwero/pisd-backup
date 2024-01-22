import os
import datetime
from crontab import CronTab

MAX_BACKUPS = 2  # Default value, can be adjusted


def info_log(message):
    print(f"[INFO] {message}")


def warning_log(message):
    print(f"[WARNING] {message}")


def add_to_sudoers():
    info_log("Configuring sudoers file...")

    # Run the add_to_sudoers.sh script with sudo
    exit_code = os.system("sudo bash src/scripts/add_sudoers_privileges.sh")

    if exit_code == 0:
        info_log("Sudoers file configured successfully.")
    else:
        warning_log("Failed to configure sudoers file.")


def install_dependencies():
    info_log("Installing dependencies...")

    # Add user to sudoers
    add_to_sudoers()

    # Install cifs-utils
    exit_code = os.system("sudo apt-get install cifs-utils")
    if exit_code == 0:
        info_log("cifs-utils installed.")
    else:
        warning_log("Failed to install cifs-utils.")

    # Create an empty file .smbServer in /root/
    smb_server_path = "/root/.smbServer"
    exit_code = os.system(f"sudo touch {smb_server_path}")
    if exit_code == 0:
        info_log(f"Created {smb_server_path}.")
    else:
        warning_log(f"Failed to create {smb_server_path}.")

    # Download pishrink.sh script and move it to /usr/local/bin/
    pishrink_path = "/usr/local/bin/pishrink.sh"
    exit_code = os.system("wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh")
    exit_code += os.system("chmod +x pishrink.sh")
    exit_code += os.system(f"sudo mv pishrink.sh {pishrink_path}")

    if exit_code == 0:
        info_log(f"Downloaded pishrink.sh and moved it to {pishrink_path}.")
    else:
        warning_log(f"Failed to download or move pishrink.sh.")


def backup_raspberry_pi():
    info_log("Backing up Raspberry Pi...")

    # Prompt user for the number of backups to keep
    max_backups = input("Enter the maximum number of backups to keep: ")
    try:
        max_backups = int(max_backups)
    except ValueError:
        warning_log("Invalid input for maximum backups. Using default value.")
        max_backups = MAX_BACKUPS

    # Set the backup filename based on the hostname, current date, hour, and minute
    bk_filename = f"{os.uname().nodename}.{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.img"
    backup_path = f"/home/{os.getlogin()}/backup-raspis/{bk_filename}"

    # Create a backup of the Raspberry Pi using dd
    exit_code = os.system(f"sudo dd bs=4M if=/dev/mmcblk0 of={backup_path}")

    if exit_code == 0:
        info_log(f"Created backup: {backup_path}")
        manage_backups(os.uname().nodename, max_backups)
    else:
        warning_log(f"Failed to create backup.")

    # Run pishrink.sh on the created backup
    exit_code = os.system(f"sudo pishrink.sh {backup_path}")

    if exit_code == 0:
        info_log("Ran pishrink.sh on the backup.")
    else:
        warning_log("Failed to run pishrink.sh.")


def setup_cronjob():
    info_log("Setting up cronjob for option 2...")

    # Get the current user's crontab
    cron = CronTab(user=os.getlogin())

    # Prompt user for custom cron schedule
    cron_schedule = input("Enter the custom cron schedule (e.g., '0 2 * * *'): ")

    # Add the cron job for option 2
    job = cron.new(command=f"sudo python3 {__file__} backup_raspberry_pi && sudo python3 {__file__} manage_backups", comment="Backup Raspberry Pi")
    job.setall(cron_schedule)

    cron.write()

    info_log(f"Cronjob added. Schedule: {cron_schedule}")


def manage_backups(hostname, max_backups):
    backup_dir = f"/home/{os.getlogin()}/backup-raspis/"
    backups = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]

    # Filter backups for the current hostname
    host_backups = [f for f in backups if f.startswith(hostname)]

    # Sort backups by modification time (oldest first)
    host_backups
    host_backups.sort(key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)))

    # Keep only the latest max_backups backups
    if len(host_backups) > max_backups:
        backups_to_delete = host_backups[:-max_backups]

        for backup in backups_to_delete:
            backup_path = os.path.join(backup_dir, backup)
            os.remove(backup_path)
            info_log(f"Deleted old backup: {backup_path}")


def main():
    while True:
        print("Choose an option:")
        print("1. Install dependencies")
        print("2. Backup Raspberry Pi")
        print("3. Setup cronjob for option 2")
        print("4. Manage number of backups")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            install_dependencies()
        elif choice == "2":
            backup_raspberry_pi()
        elif choice == "3":
            setup_cronjob()
        elif choice == "4":
            manage_backups_input = input("Enter the number of backups to keep: ")
            try:
                manage_backups_max = int(manage_backups_input)
            except ValueError:
                warning_log("Invalid input for maximum backups. Using default value.")
                manage_backups_max = MAX_BACKUPS
            manage_backups(os.uname().nodename, manage_backups_max)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
