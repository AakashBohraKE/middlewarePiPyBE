"""FastAPI middleware for comprehensive error logging.

This module provides a middleware that catches and logs all API errors,
including HTTP errors and unhandled exceptions, to a JSON file.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
import json
import time
import platform
import socket
from typing import Callable, Optional
from .logger import JSONLogger

def get_system_info() -> dict:
    """Get system information including OS, version, machine details, etc.
    
    Returns:
        dict: A dictionary containing system information.
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname()
    }

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging API errors in FastAPI applications.
    
    This middleware catches all errors (HTTP errors and exceptions) that occur
    during request processing and logs them to a JSON file with detailed
    information about the error, request, and system.
    
    Attributes:
        logger (JSONLogger): The logger instance used for error logging.
    """

    def __init__(
        self,
        app,
        log_file: str = "error_logs.json",
        log_level: str = "DEBUG",
        include_system_info: bool = True
    ):
        """Initialize the middleware.
        
        Args:
            app: The FastAPI application instance.
            log_file (str): Path to the log file. Defaults to "error_logs.json".
            log_level (str): Logging level. Defaults to "DEBUG".
            include_system_info (bool): Whether to include system information in logs.
                Defaults to True.
        """
        super().__init__(app)
        self.logger = JSONLogger(
            log_file=log_file,
            log_level=log_level,
            include_system_info=include_system_info
        )

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log any errors that occur.
        
        Args:
            request (Request): The incoming request.
            call_next (Callable): The next middleware or route handler.
            
        Returns:
            Response: The response from the next middleware or route handler.
            
        Raises:
            Exception: Any exception that occurs during request processing.
        """
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log error responses (status code >= 400)
            if response.status_code >= 400:
                error_data = {
                    "path": request.url.path,
                    "method": request.method,
                    "headers": dict(request.headers),
                    "query_params": dict(request.query_params),
                    "error_type": "HTTPError",
                    "error_message": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "traceback": "HTTP Error Response",
                    "client_ip": request.client.host if request.client else None,
                    "system_info": get_system_info() if self.logger.include_system_info else None,
                    "response_time_ms": round(process_time * 1000, 2)
                }
                self.logger.log_error(error_data)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            error_data = {
                "path": request.url.path,
                "method": request.method,
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc(),
                "client_ip": request.client.host if request.client else None,
                "system_info": get_system_info() if self.logger.include_system_info else None,
                "response_time_ms": round(process_time * 1000, 2)
            }

            self.logger.log_error(error_data)
            raise 