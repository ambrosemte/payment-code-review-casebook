"""Case 06 (Buggy): Unverified & replayable payment webhook."""

import json


def accept_webhook_buggy(raw_body: bytes, signature: str, timestamp: int, secret: str, now: int) -> dict:
    # BUG: Ignores HMAC signature and timestamp freshness completely.
    return json.loads(raw_body.decode("utf-8"))
