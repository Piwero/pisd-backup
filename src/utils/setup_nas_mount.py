import os

from src.utils.logger import info_log, warning_log


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
