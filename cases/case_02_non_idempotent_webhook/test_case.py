import pytest

from cases.case_02_non_idempotent_webhook.buggy import BuggyWebhookProcessor
from cases.case_02_non_idempotent_webhook.fixed import FixedWebhookProcessor


def _assert_idempotent_credit(proc_cls):
    proc = proc_cls()
    event = {"event_id": "EVT-1001", "user_id": "USR-1", "amount_kobo": 500_000}
    proc.handle_credit_event(event)
    proc.handle_credit_event(event)
    assert proc.balances["USR-1"] == 500_000


def test_buggy_double_credits_on_duplicate_webhook():
    with pytest.raises(AssertionError):
        _assert_idempotent_credit(BuggyWebhookProcessor)


def test_fixed_ignores_duplicate_webhook():
    _assert_idempotent_credit(FixedWebhookProcessor)
