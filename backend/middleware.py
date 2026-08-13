import time
from fastapi import Request

async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000  # Convert to Milliseconds
    print(f"[{request.method}] Path: {request.url.path} - Completed in {process_time:.2f}ms | Status: {response.status_code}")
    
    response.headers["X-Process-Time-Ms"] = str(process_time)
    return response