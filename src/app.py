import os
import datetime


def install_dependencies():
    print("Installing dependencies...")

    # Install cifs-utils
    os.system("sudo apt-get install cifs-utils")
    print("cifs-utils installed.")

    # Create an empty file .smbServer in /root/
    smb_server_path = "/root/.smbServer"
    os.system(f"sudo touch {smb_server_path}")
    print(f"Created {smb_server_path}.")

    # Download pishrink.sh script and move it to /usr/local/bin/
    pishrink_path = "/usr/local/bin/pishrink.sh"
    os.system("wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh")
    os.system("chmod +x pishrink.sh")
    os.system(f"sudo mv pishrink.sh {pishrink_path}")
    print(f"Downloaded pishrink.sh and moved it to {pishrink_path}.")


def backup_raspberry_pi():
    print("Backing up Raspberry Pi...")

    # Set the backup filename based on the hostname, current date, hour, and minute
    bk_filename = f"{os.uname().nodename}.{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.img"
    backup_path = f"/home/{os.getlogin()}/backup-raspis/{bk_filename}"

    # Create a backup of the Raspberry Pi using dd
    os.system(f"sudo dd bs=4M if=/dev/mmcblk0 of={backup_path}")
    print(f"Created backup: {backup_path}")

    # Run pishrink.sh on the created backup
    os.system(f"sudo pishrink.sh {backup_path}")
    print("Ran pishrink.sh on the backup.")


def main():
    while True:
        print("Choose an option:")
        print("1. Install dependencies")
        print("2. Backup Raspberry Pi")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            install_dependencies()
        elif choice == "2":
            backup_raspberry_pi()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
