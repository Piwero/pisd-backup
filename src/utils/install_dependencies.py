import os

from utils.logger import info_log, warning_log


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

    # Install python dependencies
    exit_code = os.system("sudo pip install python-crontab")
    if exit_code == 0:
        info_log("Successfully installed the project dependencies.")
    else:
        warning_log("Failed to install project dependencies.")

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
