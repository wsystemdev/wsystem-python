"""Small live smoke test against https://api.wsystem.dev. Opt in with WSYSTEM_LIVE=1; the key (if any) comes from WSYSTEM_API_KEY and is never printed."""
import os

import pytest

from wsystem import WSystem

pytestmark = pytest.mark.skipif(os.environ.get("WSYSTEM_LIVE") != "1", reason="set WSYSTEM_LIVE=1 to run")


def test_live():
    ws = WSystem()
    assert ws.verify_vat("BE0403170701")["status"] == "valid"
    sample = ws.einvoice_sample(type="credit_note")
    assert sample
    res = ws.create_einvoice({**(sample if isinstance(sample, dict) else {}), "format": "zugferd"}) if isinstance(sample, dict) else None
    if isinstance(res, dict):
        assert res.get("valid") is True and res.get("pdf_base64")
    assert isinstance(ws.health(), (dict, str))
