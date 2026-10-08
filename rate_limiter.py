"""Simple in-memory fixed-window rate limiter.

Suitable for local/demo use. State is process-local and is lost on restart.
"""

import logging
import threading
import time
from collections import defaultdict

from fastapi import HTTPException, Request

logger = logging.getLogger("rate_limiter")

RATE_LIMIT = 10
WINDOW_SECONDS = 60

# (client_ip, endpoint) -> list of request timestamps
_requests: dict[tuple[str, str], list[float]] = defaultdict(list)
_lock = threading.Lock()


def check_rate_limit(request: Request) -> None:
    """Allow at most RATE_LIMIT requests per client/IP and endpoint per window."""
    client_ip = request.client.host if request.client else "unknown"
    key = (client_ip, request.url.path)
    now = time.monotonic()
    window_start = now - WINDOW_SECONDS

    with _lock:
        timestamps = [ts for ts in _requests[key] if ts > window_start]

        if len(timestamps) >= RATE_LIMIT:
            retry_after = max(1, int(WINDOW_SECONDS - (now - timestamps[0])))
            logger.warning(
                "Rate limit exceeded: endpoint=%s client=%s",
                request.url.path,
                client_ip,
            )
            _requests[key] = timestamps
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
                headers={"Retry-After": str(retry_after)},
            )

        timestamps.append(now)
        _requests[key] = timestamps


def reset_rate_limiter() -> None:
    """Clear limiter state. Intended for tests only."""
    with _lock:
        _requests.clear()
