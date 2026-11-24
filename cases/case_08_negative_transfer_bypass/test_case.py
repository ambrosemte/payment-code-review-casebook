import pytest

from cases.case_08_negative_transfer_bypass.buggy import transfer_buggy
from cases.case_08_negative_transfer_bypass.fixed import transfer_fixed


def test_buggy_allows_negative_transfer_theft():
    balances = {"attacker": 0, "victim": 10_000}
    transfer_buggy(balances, "attacker", "victim", -5_000)
    assert balances["attacker"] == 5_000
    assert balances["victim"] == 5_000


def test_fixed_rejects_negative_and_zero_transfers():
    balances = {"attacker": 0, "victim": 10_000}
    with pytest.raises(ValueError):
        transfer_fixed(balances, "attacker", "victim", -5_000)
    with pytest.raises(ValueError):
        transfer_fixed(balances, "attacker", "victim", 0)
    assert balances == {"attacker": 0, "victim": 10_000}
