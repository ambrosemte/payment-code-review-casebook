from concurrent.futures import ThreadPoolExecutor
import pytest

from cases.case_01_double_charge_race.buggy import BuggyWallet
from cases.case_01_double_charge_race.fixed import FixedWallet


def _assert_no_double_spend(wallet_cls):
    wallet = wallet_cls(balance=1000)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: wallet.debit(800), range(2)))
    assert results.count(True) == 1
    assert wallet.balance == 200


def test_buggy_fails_concurrency_invariant():
    with pytest.raises(AssertionError):
        _assert_no_double_spend(BuggyWallet)


def test_fixed_passes_concurrency_invariant():
    _assert_no_double_spend(FixedWallet)
