# Concurrency Configuration

This backend is optimized to handle **50+ concurrent requests** from different users simultaneously.

## How It Works

### Thread Pool Executor
- **50 worker threads** are available for blocking I/O operations
- Each request runs independently without blocking others
- Blocking operations (Gemini API calls, PIL image processing) are executed in thread pools

### Key Optimizations

1. **Async Endpoints**: All endpoints use `async def` to allow concurrent request handling
2. **Thread Pool for Blocking I/O**: 
   - Gemini API calls run in thread pool (prevents blocking event loop)
   - PIL image processing runs in thread pool
   - Image encoding/decoding runs in thread pool
3. **Thread-Safe Model Creation**: Each thread creates its own Gemini model instance
4. **Request Tracking**: Each request has a unique ID for logging and debugging

## Running with Multiple Workers

### Option 1: Use the Production Server Script
```bash
python start_server.py
```

This will start with:
- **4 worker processes** (configurable via `WORKERS` env var)
- **50 concurrent connections per worker** (configurable via `LIMIT_CONCURRENCY` env var)
- **Total capacity: ~200 concurrent requests** (4 workers × 50 connections)

### Option 2: Use Uvicorn Directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --limit-concurrency 50
```

### Option 3: Development Mode (Single Worker)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

You can configure concurrency settings via environment variables:

```bash
# Number of worker processes (default: 4)
WORKERS=4

# Max concurrent connections per worker (default: 50)
LIMIT_CONCURRENCY=50

# Server host (default: 0.0.0.0)
HOST=0.0.0.0

# Server port (default: 8000)
PORT=8000
```

## Performance Characteristics

- **Single Request**: ~5-15 seconds (depending on Gemini API response time)
- **Concurrent Requests**: All handled in parallel without blocking
- **Memory**: Each request uses ~50-100MB (image processing + API response)
- **CPU**: Mostly I/O bound (waiting for Gemini API), minimal CPU usage

## Monitoring

Each request is logged with a unique ID:
```
[filename_12345] Received upload request: chart.png
[filename_12345] Calling Gemini API with model: nano-banana-pro-preview
[filename_12345] Analysis complete, returning results
```

This allows you to track individual requests even when handling many concurrently.

## Scaling Recommendations

- **For 50 concurrent users**: Use default settings (4 workers, 50 connections/worker)
- **For 100+ concurrent users**: Increase `WORKERS` to 8-10
- **For high-traffic production**: Consider using a load balancer (nginx) with multiple backend instances

## Rate Limiting

Note: The Gemini API may have its own rate limits. If you encounter rate limit errors:
- Implement request queuing
- Add exponential backoff retry logic
- Consider using multiple API keys with load balancing

