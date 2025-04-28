from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
import traceback
from datetime import datetime
import platform
import sys
import psutil
import time
import socket
from .logger import ErrorLogger

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, log_file_path: str = "error_logs.json"):
        super().__init__(app)
        self.logger = ErrorLogger(log_file_path)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # Calculate response time
            response_time = time.time() - start_time
            
            # Get client IP
            client_ip = request.client.host if request.client else "unknown"
            
            # Get request body if available
            try:
                body = await request.body()
                request_body = body.decode() if body else None
            except:
                request_body = None

            # Log HTTP exceptions
            error_info = {
                "timestamp": datetime.now().isoformat(),
                "path": request.url.path,
                "method": request.method,
                "query_params": dict(request.query_params),
                "headers": dict(request.headers),
                "client_ip": client_ip,
                "response_time_ms": round(response_time * 1000, 2),
                "error_type": "HTTPException",
                "error_message": http_exc.detail,
                "status_code": http_exc.status_code,
                "traceback": traceback.format_exc(),
                "request_body": request_body,
                "system_info": {
                    "python_version": sys.version,
                    "platform": platform.platform(),
                    "system": platform.system(),
                    "processor": platform.processor(),
                    "hostname": socket.gethostname(),
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent
                }
            }
            print(f"Logging HTTP error: {error_info}")  # Debug print
            self.logger.log_error(error_info)
            raise
        except Exception as e:
            # Calculate response time
            response_time = time.time() - start_time
            
            # Get client IP
            client_ip = request.client.host if request.client else "unknown"
            
            # Get request body if available
            try:
                body = await request.body()
                request_body = body.decode() if body else None
            except:
                request_body = None

            # Log other exceptions
            error_info = {
                "timestamp": datetime.now().isoformat(),
                "path": request.url.path,
                "method": request.method,
                "query_params": dict(request.query_params),
                "headers": dict(request.headers),
                "client_ip": client_ip,
                "response_time_ms": round(response_time * 1000, 2),
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc(),
                "request_body": request_body,
                "system_info": {
                    "python_version": sys.version,
                    "platform": platform.platform(),
                    "system": platform.system(),
                    "processor": platform.processor(),
                    "hostname": socket.gethostname(),
                    "cpu_percent": psutil.cpu_percent(),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent
                }
            }
            print(f"Logging general error: {error_info}")  # Debug print
            self.logger.log_error(error_info)
            raise 