from cases.case_10_secret_log_leak.buggy import format_error_log_buggy
from cases.case_10_secret_log_leak.fixed import format_error_log_fixed

PAYLOAD = {
    "user_id": "USR-99",
    "amount": 15000,
    "pin": "4821",
    "headers": {"api_secret": "sk_test_example_999"},
}


def test_buggy_exposes_pin_and_secret_in_logs():
    line = format_error_log_buggy(PAYLOAD, "gateway timeout")
    assert "4821" in line
    assert "sk_test_example_999" in line


def test_fixed_redacts_pin_and_secret():
    line = format_error_log_fixed(PAYLOAD, "gateway timeout")
    assert "4821" not in line
    assert "sk_test_example_999" not in line
    assert "[REDACTED]" in line
    assert "USR-99" in line
