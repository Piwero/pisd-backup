
** piSD-backup - Automated Raspberry Pi SD Card Backup**

**Overview**

`piSD-backup` is a Python script designed to simplify and automate the backup process for your Raspberry Pi's SD card. It provides a user-friendly interface for installing dependencies, performing backups, scheduling backups with cron jobs, and managing the number of backup files stored. This ensures that your Raspberry Pi's data is safely backed up, allowing for easy recovery in case of SD card failure or corruption.

**Key Features**

* **Automated Backups:** Easily create complete image backups of your Raspberry Pi's SD card.
* **Scheduled Backups:** Set up cron jobs to automate backups at regular intervals.
* **Dependency Management:** Automatically install required Python dependencies.
* **Backup Management:** Control the number of backup files stored, preventing excessive disk usage.
* **NAS Integration:** Seamlessly mount network-attached storage (NAS) volumes for storing backups.
* **Command-Line and Interactive Interface:** Use the script via the interactive menu or directly from the command line.

**Prerequisites**

* A Raspberry Pi running a compatible operating system (Raspbian, Raspberry Pi OS, DietPi, etc.).
* A storage location for backups (local drive or NAS).
* Basic familiarity with the Linux command line.

**Setup**

**1. Install Dependencies**

* To install the necessary Python dependencies, run the following command:

```bash
sudo python3 src/app.py install_dependencies
```

* Alternatively, use the interactive menu:

```bash
sudo python3 src/app.py
```

* Then select option `1` to install dependencies.

**2. Mount Volume from NAS (Optional)**

* If you intend to store backups on a NAS, follow these steps:
    * **Create Credentials File:**
        * Create a file named `/root/.smbServer` with your NAS credentials:

```
username=backups
password=YourSecurePassword
```

* **Important:** Replace `YourSecurePassword` with your actual NAS password. Secure file permissions should be enforced.
    * **Create Backup Directory:**
        * Create a directory on your Raspberry Pi to mount the NAS share:

```bash
mkdir backup-raspis
```

    * **Edit `/etc/fstab`:**
        * Add the following line to `/etc/fstab` to automatically mount the NAS share on boot:

```
//Your.NAS.IP.Address/backup-raspis /home/$USER/backup-raspis cifs credentials=/root/.smbServer,uid=1001 0 0
```

* **Important:** Replace `Your.NAS.IP.Address` with the actual IP address of your NAS.
    * **Mount the Share:**
        * execute `sudo mount -a` to mount the newly added fstab entry.
    * **DietPi Users:**
        * For DietPi users, use `sudo dietpi-config`, select option `14` (Autostart Options), and add `sudo mount -a` to ensure the NAS volume is mounted on startup.
        * It is also recommended that after mounting the NAS, to run `sudo dietpi-drive_manager` and use the resize option.

**Usage**

**1. Interactive Menu**

* To use the interactive menu, run:

```bash
sudo python3 src/app.py
```

* The menu provides the following options:
    * `1. Install Dependencies`
    * `2. Backup Raspberry Pi`
    * `3. Setup Cronjob for Option 2`
    * `4. Manage Number of Backups`

**2. Command-Line Options**

* You can also use command-line options for specific actions:
    * Install dependencies:

```bash
sudo python3 src/app.py install_dependencies
```

    * Backup Raspberry Pi:

```bash
sudo python3 src/app.py backup_raspberry_pi
```

    * Setup cron job:

```bash
sudo python3 src/app.py setup_cronjob
```

    * Manage number of backups:

```bash
sudo python3 src/app.py manage_backups [num_backups]
```

* Replace `[num_backups]` with the desired number of backups to keep.

**Cron Job Management**

* **View Cron Jobs:**
    * To view existing cron jobs, run:

```bash
crontab -l
```

* **Edit Cron Jobs:**
    * To edit cron jobs, run:

```bash
crontab -e
```

**Important Considerations**

* Ensure you have sufficient storage space for backups.
* Regularly test your backups to verify they are working correctly.
* When using a NAS, confirm that the NAS is powered on and accessible before scheduled backups.
* Secure your NAS credentials.
* It is best practice to unmount the NAS after the backup has completed.