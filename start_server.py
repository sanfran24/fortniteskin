"""
Production-ready server startup script with proper concurrency settings.
Run with: python start_server.py
Or use uvicorn directly: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --limit-concurrency 50
"""

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 4))  # Number of worker processes
    limit_concurrency = int(os.getenv("LIMIT_CONCURRENCY", 50))  # Max concurrent requests per worker
    
    print(f"Starting server with {workers} workers, max {limit_concurrency} concurrent requests per worker")
    print(f"Total capacity: ~{workers * limit_concurrency} concurrent requests")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,  # Multiple worker processes for better CPU utilization
        limit_concurrency=limit_concurrency,  # Max concurrent connections per worker
        backlog=2048,  # Connection backlog
        timeout_keep_alive=30,  # Keep connections alive for 30 seconds
        log_level="info",
        access_log=True,
    )

