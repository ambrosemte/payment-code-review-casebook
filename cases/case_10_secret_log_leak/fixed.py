"""Case 10 (Fixed): Redact sensitive keys before emitting structured error logs."""

import json

SENSITIVE_KEYS = {"pin", "password", "otp", "token", "api_secret", "authorization"}


def redact_payload(data: dict) -> dict:
    clean = {}
    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            clean[k] = "[REDACTED]"
        elif isinstance(v, dict):
            clean[k] = redact_payload(v)
        else:
            clean[k] = v
    return clean


def format_error_log_fixed(request_payload: dict, error_msg: str) -> str:
    safe_payload = redact_payload(request_payload)
    return f"Payment failed ({error_msg}): payload={json.dumps(safe_payload)}"
