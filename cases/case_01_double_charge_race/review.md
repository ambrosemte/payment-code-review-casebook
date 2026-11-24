# Case 01: Double-Charge / Overdraft Race Condition

- **Severity:** Critical
- **Category:** Concurrency & Ledger Integrity

## What Is Wrong
`BuggyWallet.debit()` reads `self.balance`, checks `current < amount`, and writes `current - amount` without holding a lock (or a database row lock such as `SELECT ... FOR UPDATE`).

## Why It Matters
When two identical debit requests arrive concurrently (e.g., double-tap on a mobile app or retry storm), both pass the balance check before either writes. The customer is charged twice or spends more than their available balance, breaking ledger conservation.

## How to Reproduce
Spawn two threads attempting to debit `₦800` simultaneously from a wallet holding `₦1,000`. In `buggy.py`, both succeed and the final balance is overwritten to `₦200` (effectively creating `₦600` out of thin air).

## Fix
Serialize the check-and-debit critical section using a lock (in production SQL, wrap in a transaction with `SELECT ... FOR UPDATE` or an atomic conditional update `UPDATE wallets SET balance = balance - ? WHERE id = ? AND balance >= ?`).
