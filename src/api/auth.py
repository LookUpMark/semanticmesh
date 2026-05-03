"""API key authentication dependency for FastAPI.

Usage
-----
Apply to individual routers via::

    router = APIRouter(dependencies=[Depends(require_api_key)])

Or globally on the FastAPI app::

    app = FastAPI(dependencies=[Depends(require_api_key)])

Configuration
-------------
Set ``API_KEY`` in the environment (or .env file).
If ``API_KEY`` is empty or unset, authentication is **disabled** — all requests
are allowed. This keeps local development and unit tests frictionless.

Future multi-tenant extension
------------------------------
When multi-KG support is needed, the key can be swapped for a JWT that carries
a ``tenant_id`` (or ``graph_id``). The ``require_api_key`` dependency can then
return the tenant context, which routers inject into Builder/Query calls to
route each user to their own Neo4j database or namespace.
"""

from __future__ import annotations

import logging
import os
import secrets
import time
from collections import defaultdict

from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader

_logger = logging.getLogger(__name__)

_auth_warning_logged = False
_auth_attempts: dict[str, list[float]] = defaultdict(list)

_API_KEY_HEADER = APIKeyHeader(
    name="X-API-Key",
    description=(
        "API key for authentication. "
        "Set the `API_KEY` environment variable to enable. "
        "Leave unset to disable auth (local / dev mode)."
    ),
    auto_error=False,  # we raise manually so we can give a clearer error
)


def _get_configured_key() -> str | None:
    """Return the API key from the environment, or None if not set."""
    key = os.environ.get("API_KEY", "").strip()
    return key if key else None


def require_api_key(
    request: Request, api_key: str | None = Security(_API_KEY_HEADER)
) -> str | None:
    """FastAPI dependency that validates the X-API-Key header.

    - If ``API_KEY`` env var is **not set**: auth is disabled, all requests pass.
    - If ``API_KEY`` is set: header must be present and match exactly.

    Returns the validated key (or None when auth is disabled).
    """
    configured = _get_configured_key()
    if configured is None:
        global _auth_warning_logged
        if not _auth_warning_logged:
            _logger.warning(
                "╔══════════════════════════════════════════════════════════╗\n"
                "║  API_KEY not set — authentication DISABLED.             ║\n"
                "║  All endpoints (including DELETE /graph) are UNPROTECTED.║\n"
                "║  Set API_KEY env var before deploying to production.     ║\n"
                "╚══════════════════════════════════════════════════════════╝"
            )
            _auth_warning_logged = True
        return None

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide it via the X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Rate limiting (configurable via settings)
    from src.config.settings import get_settings

    _settings = get_settings()
    _max_attempts = _settings.api_rate_limit_max_attempts
    _window_seconds = _settings.api_rate_limit_window_seconds

    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    _auth_attempts[client_ip] = [t for t in _auth_attempts[client_ip] if now - t < _window_seconds]
    if len(_auth_attempts[client_ip]) >= _max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts. Try again later.",
        )

    # constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(api_key, configured):
        _auth_attempts[client_ip].append(now)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return api_key
