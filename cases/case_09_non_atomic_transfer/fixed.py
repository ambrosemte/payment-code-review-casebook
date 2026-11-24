"""Case 09 (Fixed): Atomic database transaction rolls back debit on failure."""

import sqlite3


def transfer_atomic_fixed(conn: sqlite3.Connection, sender: str, recipient: str, amount: int) -> None:
    with conn:
        cur_debit = conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?",
            (amount, sender, amount),
        )
        if cur_debit.rowcount != 1:
            raise ValueError("Insufficient funds or unknown sender")
        cur_credit = conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, recipient),
        )
        if cur_credit.rowcount != 1:
            raise LookupError(f"Recipient '{recipient}' does not exist")
