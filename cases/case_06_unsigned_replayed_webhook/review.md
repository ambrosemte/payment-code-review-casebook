# Case 06: Unsigned and Replayable Webhook Endpoint

- **Severity:** Critical
- **Category:** Cryptography & Webhook Security

## What Is Wrong
`accept_webhook_buggy()` parses incoming JSON without verifying the HMAC-SHA256 signature or rejecting stale timestamps.

## Why It Matters
Anyone who discovers the public webhook URL can forge a `charge.success` payload and credit arbitrary wallets for free, or replay a captured older webhook indefinitely.

## How to Reproduce
Send a forged signature `"bad-sig"` or a timestamp from 1 hour ago. `buggy.py` accepts both payloads as valid.

## Fix
Bind the timestamp into the signed payload (`f"{timestamp}." + raw_body`), reject timestamps outside a narrow tolerance window (e.g., 300s), and verify the HMAC digest using `hmac.compare_digest()`.
