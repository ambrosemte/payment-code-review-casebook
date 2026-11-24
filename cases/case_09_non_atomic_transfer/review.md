# Case 09: Non-Atomic Transfer Leaving Missing Funds

- **Severity:** High
- **Category:** Transactions & Atomicity

## What Is Wrong
`transfer_non_atomic_buggy()` commits the sender's debit before attempting to credit the recipient.

## Why It Matters
If the recipient account is missing, frozen, or the process crashes mid-flight, the sender's money is permanently debited without ever reaching the recipient.

## How to Reproduce
Attempt a `₦4,000` transfer from `USR-1` (balance `₦10,000`) to a non-existent `USR-MISSING`. `buggy.py` raises `LookupError` but leaves `USR-1` at `₦6,000`.

## Fix
Wrap both updates inside a single ACID database transaction (`with conn:` in SQLite, `DB::transaction(...)` in Laravel) so any exception rolls back the debit cleanly.
