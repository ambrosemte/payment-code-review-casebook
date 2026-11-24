"""Case 07 (Fixed): Single SQL JOIN eliminating the N+1 query pattern."""

import sqlite3


def list_transactions_fixed(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT t.tx_id, u.name, t.amount
        FROM transactions t
        JOIN users u ON u.id = t.user_id
        ORDER BY t.tx_id
        """
    ).fetchall()
    return [{"tx_id": tx_id, "user_name": name, "amount": amount} for tx_id, name, amount in rows]
