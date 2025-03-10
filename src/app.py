import os
import sys

from utils.backup_raspberry_pi import backup_raspberry_pi
from utils.install_dependencies import install_dependencies
from utils.logger import warning_log
from utils.manage_backups import MAX_BACKUPS, manage_backups
from utils.setup_cronjob import setup_cronjob
from utils.setup_nas_mount import setup_nas_mount


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
            print("2. Setup NAS mount volume")
            print("3. Setup cronjob for option Backup")
            print("4. Manage number of backups")
            print("5. Backup Raspberry Pi")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                install_dependencies()
            elif choice == "2":
                setup_nas_mount()
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
                backup_raspberry_pi()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
