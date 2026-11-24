import pytest

from cases.case_04_missing_authorization_idor.buggy import BuggyReceiptService
from cases.case_04_missing_authorization_idor.fixed import FixedReceiptService

SAMPLE = {"RCPT-001": {"owner_id": "USR-A", "amount": 25000}}


def test_buggy_leaks_other_users_receipt():
    svc = BuggyReceiptService(SAMPLE)
    # Buggy version improperly returns USR-A's receipt to USR-B
    assert svc.get_receipt("USR-B", "RCPT-001")["owner_id"] == "USR-A"


def test_fixed_blocks_unauthorized_access():
    svc = FixedReceiptService(SAMPLE)
    assert svc.get_receipt("USR-A", "RCPT-001")["amount"] == 25000
    with pytest.raises(PermissionError):
        svc.get_receipt("USR-B", "RCPT-001")
