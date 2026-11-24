"""Case 07 (Buggy): N+1 SQL query when listing transactions with user names."""

import sqlite3


def list_transactions_buggy(conn: sqlite3.Connection) -> list[dict]:
    # BUG: 1 query for N transactions + N separate queries for user names.
    rows = conn.execute("SELECT tx_id, user_id, amount FROM transactions ORDER BY tx_id").fetchall()
    output = []
    for tx_id, user_id, amount in rows:
        user_name = conn.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()[0]
        output.append({"tx_id": tx_id, "user_name": user_name, "amount": amount})
    return output
