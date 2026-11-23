"""Typed errors. Every API error carries status, parsed body, error code and the request id when the API sends one."""
from __future__ import annotations
from typing import Any, Optional


class WSystemError(Exception):
    """Base class for everything this SDK raises."""


class APIConnectionError(WSystemError):
    """The request never produced an HTTP answer (DNS, TLS, refused, reset)."""


class APITimeoutError(APIConnectionError):
    """The request timed out."""


class APIStatusError(WSystemError):
    """The API answered with HTTP >= 400."""

    def __init__(self, message: str, status: int, body: Any = None, headers: Optional[dict] = None, request_id: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.body = body
        self.headers = headers or {}
        self.request_id = request_id or self.headers.get("x-request-id")
        detail = body.get("detail") if isinstance(body, dict) else None
        err = body.get("error") if isinstance(body, dict) else None
        self.code: Optional[str] = (detail.get("code") if isinstance(detail, dict) else None) or (err if isinstance(err, str) else None) or (body.get("code") if isinstance(body, dict) else None)
        self.docs_url: Optional[str] = body.get("docs_url") if isinstance(body, dict) else None


class BadRequestError(APIStatusError):
    """HTTP 400 / 422: invalid or missing input."""


class AuthenticationError(APIStatusError):
    """HTTP 401 / 403: missing, invalid or not permitted API key."""


class PaymentRequiredError(APIStatusError):
    """HTTP 402: free tier used up (get a free key or a plan, or pay per call with x402)."""


class NotFoundError(APIStatusError):
    """HTTP 404."""


class ConflictError(APIStatusError):
    """HTTP 409 (for example an idempotency key reused with a different body)."""


class RateLimitError(APIStatusError):
    """HTTP 429. retry_after is in seconds when the API sent Retry-After."""

    retry_after: Optional[float] = None


class ServerError(APIStatusError):
    """HTTP 5xx."""


def error_for(status: int) -> type:
    if status in (400, 422): return BadRequestError
    if status in (401, 403): return AuthenticationError
    if status == 402: return PaymentRequiredError
    if status == 404: return NotFoundError
    if status == 409: return ConflictError
    if status == 429: return RateLimitError
    if status >= 500: return ServerError
    return APIStatusError
