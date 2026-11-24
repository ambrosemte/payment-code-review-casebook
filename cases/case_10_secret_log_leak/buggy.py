"""Case 10 (Buggy): Logging raw API secrets and transaction PINs on failure."""

import json


def format_error_log_buggy(request_payload: dict, error_msg: str) -> str:
    # BUG: Dumps raw request payload containing api_secret and pin into logs.
    return f"Payment failed ({error_msg}): payload={json.dumps(request_payload)}"
