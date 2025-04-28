"""FastAPI Error Logger package.

A FastAPI middleware for comprehensive error logging, similar to Sentry but for local use.
This package provides a middleware that catches and logs all API errors to a JSON file
with detailed information about the error, request, and system.
"""

from .middleware import ErrorLoggingMiddleware

__version__ = "0.1.0"
__all__ = ["ErrorLoggingMiddleware"] 