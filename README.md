# wsystem (Python)

Python client for the [W System](https://wsystem.dev) API: EU VAT (VIES) and EORI validation, company registers, sanctions screening, KYB and EU e-invoicing (EN 16931, XRechnung, ZUGFeRD / Factur-X PDF, credit notes, Peppol, inbox, KSeF). No dependencies, Python 3.9+, typed (`py.typed`).

The PyPI package is coming soon. Until then install from GitHub:

```bash
pip install "git+https://github.com/wsystemdev/wsystem-python.git"
```

```python
from wsystem import WSystem

ws = WSystem()                         # no key: free tier (20 calls/day per IP); or WSystem("key") / WSYSTEM_API_KEY
ws.verify_vat("BE0403170701")["status"]   # 'valid'

# ZUGFeRD / Factur-X PDF and a credit note
pdf = ws.create_einvoice_pdf({"invoice_number": "CN-1", "type_code": "381",
                              "preceding_invoice": "RE-1", "preceding_invoice_date": "2026-10-18", ...})
open("credit-note.pdf", "wb").write(pdf)
sample = ws.einvoice_sample(type="credit_note")     # invoice | zugferd | credit_note | small_business
```

## Coverage

One method per API operation (57), named after the OpenAPI `operationId` in snake_case: `verify_vat`, `lookup_company`, `screen_sanctions`, `kyb_check`, `create_einvoice`, `validate_einvoice`, `parse_einvoice`, `send_einvoice`, `check_received_invoice`, `list_inbox_invoices`, `ksef_connect`, `create_peppol_mandate`, `list_platform_companies`, `billing_usage` and so on. `wsystem.OPERATIONS` lists them all. Path parameters and required query parameters are positional, optional query parameters are keywords, JSON bodies are a dict, raw bodies are `str` (XML) or `bytes` (PDF). `ws.request("GET", "/path")` reaches anything newer than the SDK.

Examples for every operation in curl, Python, Node and PHP: https://wsystem.dev/api-examples

## Options on every call

```python
ws.send_einvoice(body, options={"request_id": "req-1", "idempotency_key": "order-1042", "timeout": 10, "max_retries": 3, "headers": {"X-App": "x"}})
```

`request_id` is sent as `X-Request-Id` and `idempotency_key` as `Idempotency-Key`. When the API answers with an `X-Request-Id` it is available as `error.request_id`.

## Client settings

`WSystem(api_key=None, base_url=None, timeout=30.0, max_retries=2, default_headers=None, transport=None)`. Environment: `WSYSTEM_API_KEY`, `WSYSTEM_BASE_URL`. Retries (exponential backoff, `Retry-After` honoured) apply to network errors, 429, 502, 503 and 504 on GET/PUT/DELETE, and on POST only when an idempotency key is set.

## Errors

All derive from `WSystemError`: `APIConnectionError` (`APITimeoutError`), and for HTTP errors `APIStatusError` with `status`, `body`, `code`, `docs_url`, `request_id` and the subclasses `BadRequestError` (400, 422), `AuthenticationError` (401, 403), `PaymentRequiredError` (402), `NotFoundError`, `ConflictError`, `RateLimitError` (`retry_after`) and `ServerError`.

## Tests

`pip install pytest && pytest` runs the offline tests (mocked transport, all 57 operations). `WSYSTEM_LIVE=1 WSYSTEM_API_KEY=... pytest tests/test_live_smoke.py` runs a small live check.

MIT licence. https://wsystem.dev
