# Payment Code Review Casebook (10 Runnable Security & Ledger Bug Studies)

*Personal portfolio project by Ambrose Makai. All code snippets, payloads, and test fixtures are original, synthetic examples written to demonstrate structured code review, debugging, and verification. No real company names, customer data, or credentials are used.*

## Problem
Payment backends fail in ways that look harmless on the happy path: unsynchronized wallet debits double-spend under concurrency, retried webhooks double-credit balances, binary floats drift during reconciliation, and missing ownership checks expose other users' receipts.

This repository documents **10 realistic payment-flow bugs** in Python (chosen so every single case study is immediately runnable via `pytest` with zero external runtime dependencies). Each case contains:
- `buggy.py` — minimal realistic snippet containing the defect
- `review.md` — structured code review (what is wrong, why it matters, severity, how to reproduce, fix)
- `fixed.py` — corrected implementation
- `test_case.py` — automated `pytest` tests verifying that `buggy.py` reproduces the defect and `fixed.py` satisfies the invariant

## Case Summary Table

| # | Case | Severity | Category | Files |
|---|---|---|---|---|
| 01 | Double-Charge / Overdraft Race Condition | Critical | Concurrency & Ledger Integrity | [`cases/case_01_double_charge_race`](cases/case_01_double_charge_race) |
| 02 | Non-Idempotent Payment Webhook Handler | Critical | Webhooks & Idempotency | [`cases/case_02_non_idempotent_webhook`](cases/case_02_non_idempotent_webhook) |
| 03 | Binary Floating-Point Money Arithmetic | High | Data Integrity & Precision | [`cases/case_03_float_money_arithmetic`](cases/case_03_float_money_arithmetic) |
| 04 | Missing Authorization Check (IDOR / BOLA) | Critical | Access Control & Security | [`cases/case_04_missing_authorization_idor`](cases/case_04_missing_authorization_idor) |
| 05 | SQL Injection in Transaction Reference Search | Critical | Injection & Database Security | [`cases/case_05_sql_injection`](cases/case_05_sql_injection) |
| 06 | Unsigned and Replayable Webhook Endpoint | Critical | Cryptography & Webhook Security | [`cases/case_06_unsigned_replayed_webhook`](cases/case_06_unsigned_replayed_webhook) |
| 07 | N+1 Query in Transaction List Endpoint | Medium | Performance & Database Access | [`cases/case_07_n_plus_one_query`](cases/case_07_n_plus_one_query) |
| 08 | Negative Transfer Amount Validation Bypass | Critical | Input Validation & Business Logic | [`cases/case_08_negative_transfer_bypass`](cases/case_08_negative_transfer_bypass) |
| 09 | Non-Atomic Transfer Leaving Missing Funds | High | Transactions & Atomicity | [`cases/case_09_non_atomic_transfer`](cases/case_09_non_atomic_transfer) |
| 10 | Leaking Secrets and Transaction PINs in Error Logs | High | Secrets Management & Observability | [`cases/case_10_secret_log_leak`](cases/case_10_secret_log_leak) |

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run all 20 verification tests (2 per case: buggy reproduction + fixed invariant)
pytest -v
```

## Results (Actual Output)
- `pytest -v` executes **20 tests across all 10 cases** (`20 passed`):
  - 10 tests prove each `buggy.py` reproduces the exact vulnerability or ledger defect.
  - 10 tests prove each `fixed.py` passes the security, atomicity, concurrency, or performance invariant.

## Limitations
- Cases are isolated in-memory / SQLite reproductions rather than full multi-process production deployments; e.g., Case 01 uses `threading.Lock` to demonstrate serialization whereas multi-worker production systems require database-level row locks (`SELECT ... FOR UPDATE`) or conditional atomic updates.
- All 10 cases are implemented in Python for single-command `pytest` portability; Laravel/PHP and Flutter/Dart equivalents follow the same underlying patterns (`DB::transaction`, `lockForUpdate()`, `hash_equals`, parameterized Eloquent bindings).

## What I Would Do Next
- Add companion Laravel (PHPUnit) and PostgreSQL `SELECT ... FOR UPDATE` integration test variants using Docker Compose.
- Add property-based tests (Hypothesis) for transfer conservation invariants across randomized concurrent sequences.
