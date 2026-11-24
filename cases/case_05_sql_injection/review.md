# Case 05: SQL Injection in Transaction Reference Search

- **Severity:** Critical
- **Category:** Injection & Database Security

## What Is Wrong
`find_tx_by_ref_buggy()` interpolates user-supplied `reference` directly into a SQL string using an f-string.

## Why It Matters
An attacker supplying `' OR '1'='1` bypasses the `WHERE` predicate and dumps every customer's transaction records (or escalates to data modification/exfiltration in databases supporting stacked queries).

## How to Reproduce
Pass `"' OR '1'='1"` to `find_tx_by_ref_buggy()`. It returns all rows in `transactions` instead of an empty list.

## Fix
Always bind user input using parameterized placeholders (`?` in SQLite, `%s` or `$1` in PostgreSQL/MySQL).
