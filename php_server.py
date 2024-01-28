#!/data/data/com.termux/files/usr/bin/python3

import subprocess
import os
import signal
from pathlib import Path

def get_storage_permission():
    storage_path = "/data/data/com.termux/files/home/storage"
    if not os.path.exists(storage_path):
        os.system("termux-setup-storage")

def create_server_folders():
    server_path = "/data/data/com.termux/files/home/storage/downloads/server"
    php_path = os.path.join(server_path, "php")

    Path(server_path).mkdir(parents=True, exist_ok=True)
    Path(php_path).mkdir(parents=True, exist_ok=True)

    return server_path, php_path  # Return both paths

def start_php_server(server_path, php_path):
    server_command = f"php -S localhost:8080 -t {php_path}"
    process = subprocess.Popen(server_command, shell=True)

    pid_file_path = os.path.join(server_path, "php_server_pid.txt")
    with open(pid_file_path, "w") as pid_file:
        pid_file.write(str(process.pid))

    print(f"PHP server started at http://localhost:8080 with PID {process.pid}")

def stop_php_server(server_path):
    pid_file_path = os.path.join(server_path, "php_server_pid.txt")
    try:
        with open(pid_file_path, "r") as pid_file:
            pid = int(pid_file.read().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"PHP server with PID {pid} stopped.")
    except FileNotFoundError:
        print("PID file not found. The PHP server may not be running.")
    except ProcessLookupError:
        print("Process not found. The PHP server may not be running.")

def display_menu():
    print("#" * 40)
    print("#   PHP Server - Created by Shubham Ude   #")
    print("#" * 40)
    print("# Options:")
    print("#   1. Start PHP Server (Enter 'start')")
    print("#   2. Stop PHP Server (Enter 'stop')")
    print("#   3. Exit (Enter 'exit')")
    print("#" * 40)

def main():
    get_storage_permission()
    server_path, php_path = create_server_folders()  

    while True:
        display_menu()
        choice = input("Enter your choice: ").lower()

        if choice == 'start':
            start_php_server(server_path, php_path)  
        elif choice == 'stop':
            stop_php_server(server_path)
        elif choice == 'exit':
            print("Exiting PHP Server UI.")
            break
        else:
            print("Invalid choice. Please enter 'start', 'stop', or 'exit'.")

if __name__ == "__main__":
    main()

