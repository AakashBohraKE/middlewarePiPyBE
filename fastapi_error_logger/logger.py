import json
import os
from datetime import datetime

class ErrorLogger:
    def __init__(self, log_file_path: str = "error_logs.json"):
        # Get the absolute path to ensure we're writing to the correct location
        self.log_file_path = os.path.abspath(log_file_path)
        print(f"Log file path: {self.log_file_path}")  # Debug print
        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file_path):
            print(f"Creating new log file at: {self.log_file_path}")  # Debug print
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            with open(self.log_file_path, 'w') as f:
                json.dump([], f)

    def log_error(self, error_info: dict):
        try:
            print(f"Attempting to log error: {error_info}")  # Debug print
            # Read existing logs
            with open(self.log_file_path, 'r') as f:
                logs = json.load(f)
            
            # Add new log
            logs.append(error_info)
            
            # Write back to file
            with open(self.log_file_path, 'w') as f:
                json.dump(logs, f, indent=2)
            print(f"Successfully logged error to: {self.log_file_path}")  # Debug print
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")  # Debug print 