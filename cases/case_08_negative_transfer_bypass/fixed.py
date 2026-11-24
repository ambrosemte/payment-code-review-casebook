"""Case 08 (Fixed): Strict positive-amount and distinct-account validation."""


def transfer_fixed(balances: dict[str, int], sender: str, recipient: str, amount: int) -> None:
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Transfer amount must be a positive integer")
    if sender == recipient:
        raise ValueError("Cannot transfer to the same account")
    if balances[sender] < amount:
        raise ValueError("Insufficient funds")
    balances[sender] -= amount
    balances[recipient] += amount
