# piSD-backup

## Overview

This script automates the backup process for Raspberry Pi SD cards. It provides options to install dependencies, perform backups, set up cron jobs, and manage the number of backups.

## Set up

### Install Dependencies

To install the required dependencies, run the following command:

```bash
sudo python3 src/app.py
```

Option 1 will install the necessary dependencies for the project.

### Mount Volume from NAS

1. Create credentials file `/root/.smbServer` with the following content:

```
username=backups
password=Test1234
```

2. Create a folder on the Raspberry Pi:

```bash
mkdir backup-raspis
```

3. Add the following line to `/etc/fstab`:

```
//100.68.44.33/backup-raspis /home/$USER/backup-raspis cifs credentials=/root/.smbServer,uid=1001 0 0
```

Replace `100.68.44.33` with the actual IP address of your NAS.

4. For Dietpi users, run the following command to edit the autostart options:

```bash
sudo dietpi-config
```

Select option `14` for autostart options and add the following line:

```bash
sudo mount -a
```

This ensures that the NAS volume is mounted automatically on system startup.

(You might want to resize the SD card with `sudo sudo dietpi-drive_manager` resize)

## Usage

The script provides an interactive menu for various actions:

- **Install Dependencies**: Installs necessary dependencies.
- **Backup Raspberry Pi**: Creates a backup of the Raspberry Pi SD card.
- **Setup Cronjob for Option 2**: Sets up a cron job for scheduled backups.
- **Manage Number of Backups**: Allows you to manage the number of stored backups.

To run the script interactively, execute:

```bash
pip install .
sudo python3 src/app.py
[option 1 to install dependencies]
```

You can also use command-line options for specific actions:

```bash
sudo python3 src/app.py install_dependencies
sudo python3 src/app.py backup_raspberry_pi
sudo python3 src/app.py setup_cronjob
sudo python3 src/app.py manage_backups [num_backups]
```

Replace `[num_backups]` with the desired number of backups to keep.

```
