from decimal import Decimal
import pytest

from cases.case_03_float_money_arithmetic.buggy import sum_micro_fees_buggy
from cases.case_03_float_money_arithmetic.fixed import sum_micro_fees_fixed


def test_buggy_float_drifts():
    total = sum_micro_fees_buggy(["0.10", "0.20"])
    assert total != 0.30


def test_fixed_decimal_is_exact():
    assert sum_micro_fees_fixed(["0.10", "0.20"]) == Decimal("0.30")
    assert sum_micro_fees_fixed(["0.10"] * 1000) == Decimal("100.00")
