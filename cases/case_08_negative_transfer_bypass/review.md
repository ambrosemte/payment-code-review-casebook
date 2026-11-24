# Case 08: Negative Transfer Amount Validation Bypass

- **Severity:** Critical
- **Category:** Input Validation & Business Logic

## What Is Wrong
`transfer_buggy()` checks `balances[sender] < amount` without checking `amount > 0`.

## Why It Matters
If an attacker submits `amount = -5000`, `balances[sender] < -5000` is `False`, so subtracting `-5000` *credits* the attacker's wallet while *debiting* the victim's wallet.

## How to Reproduce
Call `transfer_buggy({"attacker": 0, "victim": 10000}, "attacker", "victim", -5000)`. The attacker's balance becomes `5000` and the victim's drops to `5000`.

## Fix
Validate `amount > 0` (and reject booleans, non-integers, and self-transfers) before performing any balance check or mutation.
