import os
import datetime

def install_dependencies():
    # Install cifs-utils
    os.system("sudo apt-get install cifs-utils")

    # Create an empty file .smbServer in /root/
    os.system("sudo touch /root/.smbServer")

    # Download pishrink.sh script and move it to /usr/local/bin/
    os.system("wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh")
    os.system("chmod +x pishrink.sh")
    os.system("sudo mv pishrink.sh /usr/local/bin")

def backup_raspberry_pi():
    # Set the backup filename based on the hostname and current date
    bk_filename = f"{os.uname().nodename}.{datetime.datetime.now().strftime('%Y%m%d')}.img"

    # Create a backup of the Raspberry Pi using dd
    os.system(f"sudo dd bs=4M if=/dev/mmcblk0 of=/home/{os.getlogin()}/backup-raspis/{bk_filename}")

    # Run pishrink.sh on the created backup
    os.system(f"sudo pishrink.sh /home/{os.getlogin()}/backup-raspis/{bk_filename}")

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
