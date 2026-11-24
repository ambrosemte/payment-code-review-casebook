"""Case 08 (Buggy): Missing positive-amount validation allows negative transfer theft."""


def transfer_buggy(balances: dict[str, int], sender: str, recipient: str, amount: int) -> None:
    # BUG: Does not reject amount <= 0 or self-transfers.
    if balances[sender] < amount:
        raise ValueError("Insufficient funds")
    balances[sender] -= amount
    balances[recipient] += amount
