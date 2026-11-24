import sqlite3

from cases.case_07_n_plus_one_query.buggy import list_transactions_buggy
from cases.case_07_n_plus_one_query.fixed import list_transactions_fixed


def _make_db(n: int = 25):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE transactions (tx_id INT PRIMARY KEY, user_id INT, amount INT)")
    for i in range(1, n + 1):
        conn.execute("INSERT INTO users VALUES (?, ?)", (i, f"User {i}"))
        conn.execute("INSERT INTO transactions VALUES (?, ?, ?)", (i, i, i * 1000))
    return conn


def _count_queries(fn, conn):
    queries = []
    conn.set_trace_callback(queries.append)
    result = fn(conn)
    conn.set_trace_callback(None)
    return result, len(queries)


def test_buggy_executes_n_plus_one_queries():
    conn = _make_db(25)
    _, q_count = _count_queries(list_transactions_buggy, conn)
    assert q_count == 26


def test_fixed_executes_single_join_query():
    conn = _make_db(25)
    rows, q_count = _count_queries(list_transactions_fixed, conn)
    assert len(rows) == 25
    assert q_count == 1
