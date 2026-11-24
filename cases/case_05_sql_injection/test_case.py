import sqlite3

from cases.case_05_sql_injection.buggy import find_tx_by_ref_buggy
from cases.case_05_sql_injection.fixed import find_tx_by_ref_fixed


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE transactions (tx_id TEXT, user_id TEXT, reference TEXT, amount INT)")
    conn.executemany(
        "INSERT INTO transactions VALUES (?, ?, ?, ?)",
        [
            ("TX-1", "USR-1", "REF-AAA", 5000),
            ("TX-2", "USR-2", "REF-BBB", 95000),
        ],
    )
    return conn


def test_buggy_vulnerable_to_sql_injection():
    conn = _make_db()
    rows = find_tx_by_ref_buggy(conn, "' OR '1'='1")
    assert len(rows) == 2  # Leaked all rows!


def test_fixed_blocks_sql_injection():
    conn = _make_db()
    assert find_tx_by_ref_fixed(conn, "' OR '1'='1") == []
    assert len(find_tx_by_ref_fixed(conn, "REF-AAA")) == 1
