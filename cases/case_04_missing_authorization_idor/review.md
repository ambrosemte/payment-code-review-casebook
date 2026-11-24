# Case 04: Missing Authorization Check (IDOR / BOLA)

- **Severity:** Critical
- **Category:** Access Control & Security

## What Is Wrong
`BuggyReceiptService.get_receipt()` accepts `requester_user_id` but never verifies that the fetched receipt belongs to that user.

## Why It Matters
Any authenticated user can enumerate sequential or guessed receipt IDs to read another customer's payment history, bank details, or electricity meter tokens (OWASP API1: Broken Object Level Authorization).

## How to Reproduce
Request `RCPT-001` (owned by `USR-A`) as `USR-B`. `buggy.py` returns `USR-A`'s private receipt instead of denying access.

## Fix
Enforce ownership (`receipt["owner_id"] == requester_user_id`, or `WHERE id = ? AND user_id = ?` in SQL) on every read and mutation endpoint.
