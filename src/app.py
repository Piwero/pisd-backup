import subprocess
import time
import sys

def create_sd_card_backup(source_path, nas_ip, nas_username, nas_password, nas_folder):
    start_time = time.time()

    # If source_path is not provided, use $(findmnt -no source /) as default
    if not source_path:
        source_path = subprocess.check_output(["findmnt", "-no", "source", "/"]).decode("utf-8").strip()

    # Create a timestamp for the backup file
    timestamp = subprocess.check_output(["date", "+%Y%m%d%H%M%S"]).decode("utf-8").strip()

    # Specify the NAS backup file path
    nas_backup_path = f"{nas_folder}/backup_{timestamp}.img"

    # Use dd to create a raw image of the SD card directly on the NAS with sshpass
    dd_command = f"sudo dd if={source_path} | sshpass -p '{nas_password}' ssh {nas_username}@{nas_ip} 'cat > {nas_backup_path}'"
    subprocess.run(dd_command, shell=True)

    # Use pishrink.sh on the NAS (if it's available) to shrink the image size
    pishrink_command = f"sshpass -p '{nas_password}' ssh {nas_username}@{nas_ip} 'pishrink.sh {nas_backup_path}'"
    subprocess.run(pishrink_command, shell=True)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Backup completed successfully in {elapsed_time:.2f} seconds. Backup saved at: {nas_backup_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python app.py [source_path] <nas_ip> <nas_username> <nas_password> <nas_folder>")
        sys.exit(1)

    sd_card_source = sys.argv[1] if len(sys.argv) == 6 else None
    nas_ip = sys.argv[-4]
    nas_username = sys.argv[-3]
    nas_password = sys.argv[-2]
    nas_folder = sys.argv[-1]

    create_sd_card_backup(sd_card_source, nas_ip, nas_username, nas_password, nas_folder)
