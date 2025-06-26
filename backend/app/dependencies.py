import time
from fastapi import HTTPException, status

class RateLimiter:
    def __init__(self, max_calls: int = 5, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = []
    
    def __call__(self):
        now = time.time()
        # Remove calls outside the current window
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < self.window_seconds]
        
        if len(self.calls) >= self.max_calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        self.calls.append(now)
        return True

# Create rate limiter instance
rate_limiter = RateLimiter(max_calls=5, window_seconds=60)
