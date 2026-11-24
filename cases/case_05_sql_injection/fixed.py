"""Case 05 (Fixed): Parameterized SQL query preventing SQL injection."""

import sqlite3


def find_tx_by_ref_fixed(conn: sqlite3.Connection, reference: str) -> list[tuple]:
    query = "SELECT tx_id, user_id, amount FROM transactions WHERE reference = ?"
    return conn.execute(query, (reference,)).fetchall()
