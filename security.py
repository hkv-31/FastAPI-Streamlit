"""API-key authentication and security logging."""

import logging
import os
import secrets

from fastapi import Header, HTTPException

logger = logging.getLogger("api_security")


def get_api_key() -> str:
    """Read the application API key from the environment."""
    api_key = os.getenv("API_SECURITY_KEY")
    if not api_key:
        raise RuntimeError("API_SECURITY_KEY is not set in the .env file")
    return api_key


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Require a valid X-API-Key header."""
    expected_key = get_api_key()

    if not x_api_key:
        logger.warning("Rejected request: missing API key")
        raise HTTPException(status_code=401, detail="Missing API key")

    if not secrets.compare_digest(x_api_key, expected_key):
        logger.warning("Rejected request: invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")
