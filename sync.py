import os
import sys
import time
import shutil
import logging
import filecmp

log_format = "%(asctime).19s [%(levelname)s] - %(message)s"

logging.basicConfig(filename='sync_log.txt', level=logging.INFO, format=log_format)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def sync_folders(source_folder, replica_folder):
    try:
        comparison = filecmp.dircmp(source_folder, replica_folder)

        # Create missing items in replica folder
        for missing_item in comparison.left_only:
            source_item_path = os.path.join(source_folder, missing_item)
            replica_item_path = os.path.join(replica_folder, missing_item)

            if os.path.isdir(source_item_path):
                shutil.copytree(source_item_path, replica_item_path)
                logging.info(f"Created directory: {source_item_path} -> {replica_item_path}")
            else:
                shutil.copy2(source_item_path, replica_item_path)
                logging.info(f"Created file: {source_item_path} -> {replica_item_path}")

        # Remove extra items from replica folder
        for extra_item in comparison.right_only:
            extra_item_path = os.path.join(replica_folder, extra_item)
            if os.path.isdir(extra_item_path):
                shutil.rmtree(extra_item_path)
                logging.info(f"Removed directory: {extra_item_path}")
            else:
                os.remove(extra_item_path)
                logging.info(f"Removed file: {extra_item_path}")

        # Recursively synchronize subdirectories and files based on differences
        for common_dir in comparison.common_dirs:
            sync_folders(
                os.path.join(source_folder, common_dir),
                os.path.join(replica_folder, common_dir)
            )

        for diff_file in comparison.diff_files:
            source_item_path = os.path.join(source_folder, diff_file)
            replica_item_path = os.path.join(replica_folder, diff_file)
            
            shutil.copy2(source_item_path, replica_item_path)
            logging.info(f"Copied changes: {source_item_path} -> {replica_item_path}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def main():
    if sys.argv[1] == 'logcl':
        print('Cleaning log...')
        time.sleep(1)
        open('sync_log.txt', 'w').close()
        print('Log file "sync_log.txt" cleared')
        sys.exit(0)

    if len(sys.argv) != 4:
        print("Usage: python sync.py source_folder replica_folder sync_interval(seconds)")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    sync_interval = int(sys.argv[3])

    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    logging.info(f"Starting synchronization from {source_folder} to {replica_folder} every {sync_interval} seconds.")
    
    try:
        while True:
            time.sleep(sync_interval)
            sync_folders(source_folder, replica_folder)
            logging.info("Synchronization complete.")
    except KeyboardInterrupt:
        print("Stopping the synchronization...")
        time.sleep(1) 

if __name__ == "__main__":
    main()
