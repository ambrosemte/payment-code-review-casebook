"""Case 09 (Buggy): Non-atomic transfer commits debit before credit fails."""

import sqlite3


def transfer_non_atomic_buggy(conn: sqlite3.Connection, sender: str, recipient: str, amount: int) -> None:
    # BUG: Commits debit separately; if credit fails, money vanishes.
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, sender))
    conn.commit()
    cur = conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, recipient))
    if cur.rowcount != 1:
        raise LookupError(f"Recipient '{recipient}' does not exist")
    conn.commit()
