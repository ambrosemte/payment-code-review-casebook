"""Case 05 (Buggy): SQL injection via string interpolation in transaction lookup."""

import sqlite3


def find_tx_by_ref_buggy(conn: sqlite3.Connection, reference: str) -> list[tuple]:
    # BUG: Unescaped string interpolation allows SQL injection.
    query = f"SELECT tx_id, user_id, amount FROM transactions WHERE reference = '{reference}'"
    return conn.execute(query).fetchall()
