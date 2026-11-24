"""Case 03 (Buggy): Binary float arithmetic causing ledger drift."""


def sum_micro_fees_buggy(amounts: list[str]) -> float:
    # BUG: Using binary float accumulates IEEE-754 representation drift.
    total = 0.0
    for amt in amounts:
        total += float(amt)
    return total
