import os

from crontab import CronTab

from src.utils.logger import info_log


def setup_cronjob(cron_schedule):
    info_log("Setting up cronjob for option 2...")

    # Get the current user's username
    username = os.getlogin()

    # Get the path to the script
    script_path = os.path.abspath(__file__)

    # Add the cron job for option 2 with output redirection
    cron_command = f"sudo mount -a && sudo python3 {script_path} backup_raspberry_pi && sudo python3 {script_path} manage_backups"

    # Use a specific log file path or /dev/null if you don't need the output
    # Replace /path/to/logfile with the desired log file path

    # Create a new cron tab
    cron = CronTab(user=username)

    # Add the cron job for option 2
    job = cron.new(command=cron_command, comment="Backup Raspberry Pi")
    job.setall(cron_schedule)

    cron.write()

    info_log(f"Cronjob added. Schedule: {cron_schedule}")
