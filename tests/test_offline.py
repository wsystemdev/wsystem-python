import base64
import inspect
import json

import pytest

import wsystem
from wsystem import WSystem, OPERATIONS


class Fake:
    def __init__(self, *responses):
        self.responses = list(responses) or [(200, {"content-type": "application/json"}, b"{}")]
        self.calls = []

    def __call__(self, method, url, headers, body, timeout):
        self.calls.append(dict(method=method, url=url, headers=headers, body=body, timeout=timeout))
        r = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
        if isinstance(r, Exception):
            raise r
        return r


def j(status, obj, **h):
    return (status, {"content-type": "application/json", **{k.lower().replace("_", "-"): v for k, v in h.items()}}, json.dumps(obj).encode())


def client(*responses, **kw):
    f = Fake(*responses)
    kw.setdefault("sleep", lambda s: None)
    return WSystem("k_test", transport=f, **kw), f


def snake(n):
    import re
    return re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower()


def test_all_57_operations_exist_and_route():
    assert len(OPERATIONS) == 57
    for op_id, method, path in OPERATIONS:
        ws, f = client(j(200, {"ok": True}))
        fn = getattr(ws, snake(op_id))
        sig = inspect.signature(fn)
        args = []
        for name, p in sig.parameters.items():
            if p.kind == p.POSITIONAL_OR_KEYWORD:
                args.append("body" if name == "body" and False else ({"a": 1} if name == "body" else "x1"))
        assert fn(*args) == {"ok": True}, op_id
        c = f.calls[0]
        assert c["method"] == method, op_id
        assert c["url"].split("?")[0].count("/") == path.count("/") + 2, op_id  # https://host/... + same segments
        assert c["headers"]["X-API-Key"] == "k_test"


def test_path_and_query_encoding():
    ws, f = client()
    ws.verify_vat("BE0403170701", nocache=True, requester=None)
    assert f.calls[0]["url"] == "https://api.wsystem.dev/verify?vat=BE0403170701&nocache=true"
    ws.get_peppol_mandate("a/b c")
    assert f.calls[1]["url"].endswith("/einvoice/mandates/a%2Fb%20c")


def test_json_xml_pdf_bodies():
    ws, f = client()
    ws.create_einvoice({"format": "zugferd", "invoice_number": "1"})
    assert f.calls[0]["headers"]["Content-Type"] == "application/json" and json.loads(f.calls[0]["body"])["format"] == "zugferd"
    ws.validate_einvoice("<Invoice/>")
    assert f.calls[1]["headers"]["Content-Type"] == "application/xml"
    ws.validate_einvoice(b"%PDF-1.7 ...")
    assert f.calls[2]["headers"]["Content-Type"] == "application/pdf"


def test_credit_note_and_sample_and_pdf_helper():
    pdf = b"%PDF-1.7 test"
    ws, f = client(j(200, {"valid": True, "pdf_base64": base64.b64encode(pdf).decode(), "xml": "<x/>"}))
    out = ws.create_einvoice_pdf({"type_code": "381", "preceding_invoice": "RE-1", "preceding_invoice_date": "2026-11-01"})
    assert out == pdf
    body = json.loads(f.calls[0]["body"])
    assert body["format"] == "zugferd" and body["type_code"] == "381" and body["preceding_invoice"] == "RE-1"
    ws.einvoice_sample(type="credit_note")
    assert f.calls[1]["url"].endswith("/einvoice/sample?type=credit_note")
    with pytest.raises(ValueError):
        wsystem.decode_pdf({"valid": True})


def test_request_id_and_idempotency_headers_pass_through():
    ws, f = client()
    ws.send_einvoice({"x": 1}, options={"request_id": "req-1", "idempotency_key": "idem-1", "headers": {"X-Trace": "t"}})
    h = f.calls[0]["headers"]
    assert h["X-Request-Id"] == "req-1" and h["Idempotency-Key"] == "idem-1" and h["X-Trace"] == "t"
    assert h["User-Agent"].startswith("wsystem-python/")


def test_typed_errors():
    cases = [(400, wsystem.BadRequestError), (422, wsystem.BadRequestError), (401, wsystem.AuthenticationError), (403, wsystem.AuthenticationError),
             (402, wsystem.PaymentRequiredError), (404, wsystem.NotFoundError), (409, wsystem.ConflictError), (500, wsystem.ServerError)]
    for status, cls in cases:
        ws, f = client(j(status, {"detail": "nope", "docs_url": "https://api.wsystem.dev/docs#x"}, X_Request_Id="srv-9"), max_retries=0)
        with pytest.raises(cls) as e:
            ws.verify_vat("x")
        assert e.value.status == status and e.value.request_id == "srv-9" and e.value.docs_url and isinstance(e.value, wsystem.WSystemError)
    ws, _ = client(j(402, {"detail": "x"}))
    with pytest.raises(wsystem.PaymentRequiredError, match="free-key"):
        ws.verify_vat("x")


def test_retry_get_on_503_then_ok_and_retry_after():
    sleeps = []
    ws, f = client(j(503, {"detail": "down"}), j(429, {"detail": "slow"}, Retry_After="2"), j(200, {"ok": 1}), sleep=sleeps.append)
    assert ws.vies_status() == {"ok": 1}
    assert len(f.calls) == 3 and sleeps[1] == 2.0


def test_post_not_retried_without_idempotency_key_but_retried_with():
    ws, f = client(j(503, {"detail": "down"}), j(200, {"ok": 1}))
    with pytest.raises(wsystem.ServerError):
        ws.send_einvoice({"a": 1})
    assert len(f.calls) == 1
    ws, f = client(j(503, {"detail": "down"}), j(200, {"ok": 1}))
    assert ws.send_einvoice({"a": 1}, options={"idempotency_key": "k"}) == {"ok": 1}
    assert len(f.calls) == 2 and f.calls[0]["headers"]["Idempotency-Key"] == f.calls[1]["headers"]["Idempotency-Key"]


def test_retries_exhausted_raises_rate_limit_with_retry_after():
    ws, f = client(j(429, {"detail": "slow"}, Retry_After="3"), max_retries=1)
    with pytest.raises(wsystem.RateLimitError) as e:
        ws.vies_status()
    assert e.value.retry_after == 3.0 and len(f.calls) == 2


def test_connection_and_timeout_errors():
    ws, f = client(wsystem.APITimeoutError("t"), max_retries=1)
    with pytest.raises(wsystem.APITimeoutError):
        ws.vies_status()
    assert len(f.calls) == 2 and isinstance(wsystem.APITimeoutError("x"), wsystem.APIConnectionError)


def test_options_override_timeout_and_base_url_env(monkeypatch):
    ws, f = client(timeout=7)
    ws.vies_status()
    ws.vies_status(options={"timeout": 2})
    assert [c["timeout"] for c in f.calls] == [7.0, 2.0]
    monkeypatch.setenv("WSYSTEM_BASE_URL", "http://localhost:9/")
    monkeypatch.setenv("WSYSTEM_API_KEY", "from_env")
    ws = WSystem(transport=Fake())
    assert ws.base_url == "http://localhost:9" and ws.api_key == "from_env"


def test_text_responses_and_raw_request():
    ws, f = client((200, {"content-type": "application/xml"}, b"<Invoice/>"))
    assert ws.einvoice_sample() == "<Invoice/>"
    assert ws.request("get", "/health") == "<Invoice/>"


def test_current_api_error_shape_error_message_docs():
    ws, _ = client(j(400, {"error": "missing_input", "message": "needs input", "docs": "https://api.wsystem.dev/docs"}), max_retries=0)
    with pytest.raises(wsystem.BadRequestError) as e:
        ws.validate_einvoice({})
    assert e.value.code == "missing_input" and "needs input" in str(e.value) and e.value.docs_url == "https://api.wsystem.dev/docs"
    assert e.value.request_id is None  # the API does not send X-Request-Id yet; surfaced automatically once it does
