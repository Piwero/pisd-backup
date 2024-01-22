import os
import datetime
from crontab import CronTab

def info_log(message):
    print(f"[INFO] {message}")

def warning_log(message):
    print(f"[WARNING] {message}")

def add_to_sudoers():
    info_log("Configuring sudoers file...")

    # Run the add_to_sudoers.sh script with sudo
    exit_code = os.system("sudo bash add_to_sudoers.sh")

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

    # Install python-crontab
    exit_code = os.system("pip install python-crontab")
    if exit_code == 0:
        info_log("python-crontab installed.")
    else:
        warning_log("Failed to install python-crontab.")

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
        warning_log("Failed to download or move pishrink.sh.")

def backup_raspberry_pi():
    info_log("Backing up Raspberry Pi...")

    # Set the backup filename based on the hostname, current date, hour, and minute
    bk_filename = f"{os.uname().nodename}.{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.img"
    backup_path = f"/home/{os.getlogin()}/backup-raspis/{bk_filename}"

    # Create a backup of the Raspberry Pi using dd
    exit_code = os.system(f"sudo dd bs=4M if=/dev/mmcblk0 of={backup_path}")

    if exit_code == 0:
        info_log(f"Created backup: {backup_path}")
    else:
        warning_log("Failed to create backup.")

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
    job = cron.new(command=f"sudo python3 {__file__} backup_raspberry_pi", comment="Backup Raspberry Pi")
    job.setall(cron_schedule)

    cron.write()

    info_log(f"Cronjob added. Schedule: {cron_schedule}")

def main():
    while True:
        print("Choose an option:")
        print("1. Install dependencies")
        print("2. Backup Raspberry Pi")
        print("3. Setup cronjob for option 2")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            install_dependencies()
        elif choice == "2":
            backup_raspberry_pi()
        elif choice == "3":
            setup_cronjob()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
