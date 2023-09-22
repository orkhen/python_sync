Folder Synchronization Script

# Overview
This Python script provides a simple way to synchronize two folders: a source folder and a replica folder. It is designed to maintain an identical copy of the source folder within the replica folder while following specific criteria:

* Synchronization is one-way: changes in the source folder are reflected in the replica folder.
* Synchronization can be performed periodically.
* File creation, copying, and removal operations are logged to a file and console output.
* Folder paths, synchronization interval, and log file path are provided using command-line arguments.
* The script aims to minimize unnecessary copying and deletion operations for efficiency.

# Usage
1. Run the script with the following command:

```python sync.py source_folder replica_folder sync_interval(seconds)```

* __source_folder__: The path to the source folder you want to synchronize.
* __replica_folder__: The path to the replica folder where the synchronization will be reflected.
* __sync_interval__: The synchronization interval in seconds.

2. If the __replica_folder__ does not exist, the script will create it in the current or the given directory.
   
3. The script will continuously monitor and synchronize the folders at the specified interval.

# Additional Features
* Clear the log file: To clear the log file, you can use the following command:

Copy code
```python sync.py logcl```

This will clear the log file "sync_log.txt."

* Graceful exit: You can stop the synchronization gracefully by pressing Ctrl+C.

# Log File
The script logs all synchronization activities in the "sync_log.txt" file. It uses the following log format:

```yyyy-MM-dd hh:MM:ss [INFO] - Log message```

# Dependencies
This script relies on the Python standard library, so no third-party libraries are required for folder synchronization.
