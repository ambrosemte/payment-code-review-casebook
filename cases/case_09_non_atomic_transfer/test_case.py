import sqlite3
import pytest

from cases.case_09_non_atomic_transfer.buggy import transfer_non_atomic_buggy
from cases.case_09_non_atomic_transfer.fixed import transfer_atomic_fixed


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (id TEXT PRIMARY KEY, balance INT)")
    conn.execute("INSERT INTO accounts VALUES ('USR-1', 10000)")
    conn.commit()
    return conn


def test_buggy_loses_money_on_failed_credit():
    conn = _make_db()
    with pytest.raises(LookupError):
        transfer_non_atomic_buggy(conn, "USR-1", "USR-MISSING", 4000)
    bal = conn.execute("SELECT balance FROM accounts WHERE id = 'USR-1'").fetchone()[0]
    assert bal == 6000  # 4000 vanished!


def test_fixed_rolls_back_on_failed_credit():
    conn = _make_db()
    with pytest.raises(LookupError):
        transfer_atomic_fixed(conn, "USR-1", "USR-MISSING", 4000)
    bal = conn.execute("SELECT balance FROM accounts WHERE id = 'USR-1'").fetchone()[0]
    assert bal == 10000
