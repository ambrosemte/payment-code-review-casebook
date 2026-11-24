# Case 07: N+1 Query in Transaction List Endpoint

- **Severity:** Medium
- **Category:** Performance & Database Access

## What Is Wrong
`list_transactions_buggy()` fetches `N` transactions and then executes `SELECT name FROM users WHERE id = ?` inside a Python loop for every row.

## Why It Matters
Loading a 50-row admin transaction page fires 51 SQL round trips instead of 1. Under peak month-end load, this exhausts database connection pools and spikes API latency.

## How to Reproduce
Attach a SQLite trace callback (`conn.set_trace_callback`) and list 25 transactions. `buggy.py` executes 26 SQL statements; `fixed.py` executes 1.

## Fix
Use an explicit `JOIN` (or eager loading such as Laravel's `Transaction::with('user')`) to retrieve all needed fields in a single query.
