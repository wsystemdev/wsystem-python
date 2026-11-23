from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, Optional, Tuple
from urllib.parse import quote, urlencode

from .errors import APIConnectionError, APIStatusError, APITimeoutError, RateLimitError, error_for

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    TypedDict = dict  # type: ignore


class RequestOptions(TypedDict, total=False):
    """Per-request overrides accepted by every operation as options={...}."""

    headers: Dict[str, str]
    timeout: float
    max_retries: int
    request_id: str  # sent as X-Request-Id
    idempotency_key: str  # sent as Idempotency-Key


# transport(method, url, headers, body, timeout) -> (status, response headers (lower-case keys), body bytes)
Transport = Callable[[str, str, Dict[str, str], Optional[bytes], float], Tuple[int, Dict[str, str], bytes]]

RETRY_STATUS = (429, 502, 503, 504)
IDEMPOTENT = ("GET", "HEAD", "PUT", "DELETE", "OPTIONS")


def _seg(value: Any) -> str:
    return quote(str(value), safe="")


def default_transport(method: str, url: str, headers: Dict[str, str], body: Optional[bytes], timeout: float):
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 (https base url)
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read()
    except TimeoutError as e:
        raise APITimeoutError(f"W System API request timed out after {timeout}s") from e
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            raise APITimeoutError(f"W System API request timed out after {timeout}s") from e
        raise APIConnectionError(f"W System API request failed: {e.reason}") from e
    except OSError as e:
        raise APIConnectionError(f"W System API request failed: {e}") from e


def encode_body(body: Any) -> Tuple[Optional[bytes], Optional[str]]:
    """dict/list -> JSON; str -> XML (or PDF when it starts with %PDF); bytes -> PDF or XML by magic bytes."""
    if body is None:
        return None, None
    if isinstance(body, (bytes, bytearray)):
        b = bytes(body)
        return b, "application/pdf" if b.startswith(b"%PDF") else "application/xml"
    if isinstance(body, str):
        return body.encode("utf-8"), "application/pdf" if body.startswith("%PDF") else "application/xml"
    return json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), "application/json"


def _q(v: Any) -> str:
    return "true" if v is True else "false" if v is False else str(v)


def parse_body(raw: bytes, headers: Dict[str, str]) -> Any:
    text = raw.decode("utf-8", "replace")
    if not text:
        return None
    ctype = headers.get("content-type", "")
    if "json" in ctype or not ctype:
        try:
            return json.loads(text)
        except ValueError:
            return text
    return text


def backoff(attempt: int, retry_after: Optional[float]) -> float:
    if retry_after is not None:
        return min(max(retry_after, 0.0), 30.0)
    return min(0.5 * (2 ** attempt), 8.0) * (0.75 + random.random() / 2)


def send(client: "Any", method: str, path: str, query: Any, body: Any, options: Optional[RequestOptions]) -> Any:
    opts = options or {}
    q = {k: _q(v) for k, v in (query or {}).items() if v is not None}
    url = client.base_url + path + ("?" + urlencode(q) if q else "")
    headers = {"Accept": "application/json", "User-Agent": client.user_agent}
    headers.update(client.default_headers)
    if client.api_key:
        headers["X-API-Key"] = client.api_key
    data, ctype = encode_body(body)
    if ctype:
        headers["Content-Type"] = ctype
    if opts.get("request_id"):
        headers["X-Request-Id"] = opts["request_id"]
    if opts.get("idempotency_key"):
        headers["Idempotency-Key"] = opts["idempotency_key"]
    headers.update(opts.get("headers") or {})
    timeout = float(opts.get("timeout", client.timeout))
    retries = int(opts.get("max_retries", client.max_retries))
    # POST is only retried when the caller gave an Idempotency-Key (otherwise a retry could duplicate work)
    can_retry = method in IDEMPOTENT or any(k.lower() == "idempotency-key" for k in headers)
    attempt = 0
    while True:
        try:
            status, rh, raw = client.transport(method, url, headers, data, timeout)
        except APIConnectionError:
            if can_retry and attempt < retries:
                client.sleep(backoff(attempt, None)); attempt += 1; continue
            raise
        if status in RETRY_STATUS and can_retry and attempt < retries:
            ra = rh.get("retry-after")
            try:
                ra_f = float(ra) if ra is not None else None
            except ValueError:
                ra_f = None
            client.sleep(backoff(attempt, ra_f)); attempt += 1; continue
        break
    parsed = parse_body(raw, rh)
    if status >= 400:
        if status == 402:
            msg = "Free tier used up (HTTP 402). Get a free key (500 units/month) at https://api.wsystem.dev/account/free-key or a plan at https://wsystem.dev/pricing"
        else:
            detail = (parsed.get("detail") or parsed.get("message") or parsed.get("error") or parsed) if isinstance(parsed, dict) else parsed
            msg = f"W System API HTTP {status}: {detail if isinstance(detail, str) else json.dumps(detail)}"
        err = error_for(status)(msg, status, parsed, rh)
        if isinstance(err, RateLimitError):
            try:
                err.retry_after = float(rh.get("retry-after", ""))
            except ValueError:
                err.retry_after = None
        raise err
    return parsed
