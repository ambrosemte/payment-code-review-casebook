import hashlib
import hmac
import pytest

from cases.case_06_unsigned_replayed_webhook.buggy import accept_webhook_buggy
from cases.case_06_unsigned_replayed_webhook.fixed import accept_webhook_fixed

SECRET = "test-webhook-secret"
BODY = b'{"event":"charge.success","amount":50000}'


def _sign(ts: int) -> str:
    return hmac.new(SECRET.encode(), f"{ts}.".encode() + BODY, hashlib.sha256).hexdigest()


def test_buggy_accepts_forged_and_replayed_webhooks():
    assert accept_webhook_buggy(BODY, "forged-sig", 1000, SECRET, now=5000)["amount"] == 50000


def test_fixed_enforces_signature_and_freshness():
    now = 1_700_000_000
    good_sig = _sign(now - 30)
    assert accept_webhook_fixed(BODY, good_sig, now - 30, SECRET, now=now)["amount"] == 50000

    with pytest.raises(PermissionError):
        accept_webhook_fixed(BODY, "forged-sig", now - 30, SECRET, now=now)

    stale_ts = now - 3600
    with pytest.raises(PermissionError):
        accept_webhook_fixed(BODY, _sign(stale_ts), stale_ts, SECRET, now=now)
