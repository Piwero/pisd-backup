#!/bin/bash

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run the script with sudo."
    exit 1
fi

# Get the current username
current_user=$SUDO_USER

# Check if the lines are already present in the sudoers file
if grep -Fxq "$current_user ALL=(ALL) NOPASSWD: ALL" /etc/sudoers; then
    echo "Lines are already present in sudoers file. No changes needed."
else
    # Add the lines to the sudoers file
    echo "$current_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
    echo "Lines added to sudoers file."
fi
