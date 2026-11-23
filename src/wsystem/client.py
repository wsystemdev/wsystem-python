from __future__ import annotations

import base64
import os
import time
from typing import Any, Callable, Dict, Optional

from . import __version__
from ._generated import _Operations
from ._http import RequestOptions, Transport, default_transport, send

DEFAULT_BASE_URL = "https://api.wsystem.dev"


class WSystem(_Operations):
    """Client for the W System API (EU VAT/VIES, EORI, company registers, sanctions, KYB, EU e-invoicing).

    >>> ws = WSystem()                       # no key: free tier, 20 calls/day per IP
    >>> ws.verify_vat("BE0403170701")["status"]
    'valid'

    Every operation also takes options={"request_id": ..., "idempotency_key": ..., "headers": {...}, "timeout": 5, "max_retries": 0}.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        default_headers: Optional[Dict[str, str]] = None,
        transport: Optional[Transport] = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.api_key = api_key or os.environ.get("WSYSTEM_API_KEY") or None
        self.base_url = (base_url or os.environ.get("WSYSTEM_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = dict(default_headers or {})
        self.transport = transport or default_transport
        self.sleep = sleep
        self.user_agent = f"wsystem-python/{__version__}"

    def _request(self, method: str, path: str, *, query: Any = None, body: Any = None, options: Optional[RequestOptions] = None) -> Any:
        return send(self, method, path, query, body, options)

    def request(self, method: str, path: str, *, query: Any = None, body: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Call any endpoint directly (for endpoints newer than this SDK)."""
        return self._request(method.upper(), path, query=query, body=body, options=options)

    # --- convenience wrappers over generated operations ---

    def create_einvoice_pdf(self, invoice: Dict[str, Any], *, options: Optional[RequestOptions] = None) -> bytes:
        """Create a ZUGFeRD / Factur-X PDF (format 'zugferd'); returns the PDF bytes. The XML is in the full create_einvoice() answer."""
        res = self.create_einvoice({**invoice, "format": invoice.get("format") or "zugferd"}, options=options)
        return decode_pdf(res)


def decode_pdf(result: Dict[str, Any]) -> bytes:
    """PDF bytes from a /einvoice/create answer made with format zugferd / zugferd-xrechnung."""
    b64 = result.get("pdf_base64") if isinstance(result, dict) else None
    if not b64:
        raise ValueError("answer has no pdf_base64 (use format 'zugferd')")
    return base64.b64decode(b64)
