# Case 03: Binary Floating-Point Money Arithmetic

- **Severity:** High
- **Category:** Data Integrity & Precision

## What Is Wrong
`sum_micro_fees_buggy()` converts currency strings to Python `float` and sums them directly.

## Why It Matters
IEEE-754 binary floats cannot represent base-10 fractions like `0.10` or `0.20` exactly. Across thousands of fee settlements, rounding drift breaks reconciliation checks (`sum(debits) != sum(credits)`).

## How to Reproduce
Sum `["0.10", "0.20"]` (or 1,000 fees of `"0.10"`). In `buggy.py`, `0.1 + 0.2 == 0.30000000000000004 != 0.30`.

## Fix
Use `decimal.Decimal` (initialized from strings, never floats) or integer minor units (kobo/cents) for all money math.
