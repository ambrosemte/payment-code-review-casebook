"""Case 06 (Fixed): Constant-time HMAC-SHA256 verification + replay window check."""

import hashlib
import hmac
import json


def accept_webhook_fixed(
    raw_body: bytes,
    signature: str,
    timestamp: int,
    secret: str,
    now: int,
    max_age_seconds: int = 300,
) -> dict:
    if abs(now - timestamp) > max_age_seconds:
        raise PermissionError("Stale or future webhook timestamp (possible replay)")
    signed_payload = f"{timestamp}.".encode("utf-8") + raw_body
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise PermissionError("Invalid webhook signature")
    return json.loads(raw_body.decode("utf-8"))
