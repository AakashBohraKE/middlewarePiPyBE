"""JSON logger for FastAPI error logging.

This module provides a JSON logger that formats and writes error information
to a JSON file in a structured and readable format.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class JSONLogger:
    """Logger for writing error information to a JSON file.
    
    This logger formats error data into a structured JSON format and writes it
    to a specified file. It includes features like log level configuration and
    optional system information inclusion.
    
    Attributes:
        log_file (Path): Path to the log file.
        logger (Logger): The Python logger instance.
        include_system_info (bool): Whether to include system information in logs.
    """

    def __init__(
        self,
        log_file: str = "error_logs.json",
        log_level: str = "DEBUG",
        include_system_info: bool = True
    ):
        """Initialize the JSON logger.
        
        Args:
            log_file (str): Path to the log file. Defaults to "error_logs.json".
            log_level (str): Logging level. Defaults to "DEBUG".
            include_system_info (bool): Whether to include system information in logs.
                Defaults to True.
                
        Raises:
            ValueError: If the specified log level is invalid.
        """
        self.log_file = Path(log_file)
        self.logger = logging.getLogger(__name__)
        self.include_system_info = include_system_info
        
        # Set up logging level
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        logging.basicConfig(level=numeric_level)
        
        self.setup_logger()
        self.logger.debug(f"Initialized JSONLogger with log file: {log_file}")

    def setup_logger(self) -> None:
        """Set up the logger by creating the log file if it doesn't exist."""
        # Create log file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.write_text("[]")
            self.logger.debug("Created new error log file")

    def format_error_data(self, error_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format error data into a structured JSON format.
        
        Args:
            error_data (Dict[str, Any]): The raw error data to format.
            
        Returns:
            Dict[str, Any]: The formatted error data in a structured JSON format.
        """
        formatted_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_details": {
                "type": error_data.get("error_type", "Unknown"),
                "message": error_data.get("error_message", "No message"),
                "status_code": error_data.get("status_code", None),
                "traceback": error_data.get("traceback", "No traceback")
            },
            "request_details": {
                "path": error_data.get("path", "Unknown"),
                "method": error_data.get("method", "Unknown"),
                "client_ip": error_data.get("client_ip", "Unknown"),
                "response_time_ms": error_data.get("response_time_ms", 0)
            }
        }

        # Add system info if enabled
        if self.include_system_info and error_data.get("system_info"):
            formatted_data["system_info"] = error_data["system_info"]

        # Add additional info
        formatted_data["additional_info"] = {
            "headers": error_data.get("headers", {}),
            "query_params": error_data.get("query_params", {})
        }

        return formatted_data

    def log_error(self, error_data: Dict[str, Any]) -> None:
        """Log an error to the JSON file.
        
        Args:
            error_data (Dict[str, Any]): The error data to log.
        """
        try:
            self.logger.debug(f"Attempting to log error: {error_data}")
            
            # Read existing logs
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []

            # Format and append new error
            formatted_data = self.format_error_data(error_data)
            logs.append(formatted_data)

            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            self.logger.debug(f"Successfully logged error to {self.log_file}")

        except Exception as e:
            self.logger.error(f"Failed to log error: {str(e)}")
            self.logger.exception("Full traceback:") 