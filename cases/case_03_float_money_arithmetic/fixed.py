"""Case 03 (Fixed): Exact Decimal arithmetic for monetary calculations."""

from decimal import Decimal, ROUND_HALF_UP


def sum_micro_fees_fixed(amounts: list[str]) -> Decimal:
    total = Decimal("0.00")
    for amt in amounts:
        total += Decimal(amt)
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
