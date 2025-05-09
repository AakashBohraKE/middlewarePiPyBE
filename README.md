# FastAPI Error Logger

A FastAPI middleware for comprehensive error logging that captures API errors, request information, and system details.

## Installation

```bash
pip install -e .
```

## Usage

```python
from fastapi import FastAPI
from fastapi_error_logger.middleware import ErrorLoggingMiddleware

app = FastAPI()

# Add the middleware
app.add_middleware(ErrorLoggingMiddleware)

# Your routes here
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Features

- Logs API errors with detailed information
- Captures request details (method, path, headers, body)
- Records system information (OS, Python version, etc.)
- Saves logs in JSON format
- Configurable log file path

## License

MIT 