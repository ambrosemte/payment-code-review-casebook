# Case 02: Non-Idempotent Payment Webhook Handler

- **Severity:** Critical
- **Category:** Webhooks & Idempotency

## What Is Wrong
`BuggyWebhookProcessor.handle_credit_event()` credits the user's wallet every time a webhook arrives without tracking whether `event_id` has already been settled.

## Why It Matters
Payment gateways guarantee *at-least-once* webhook delivery. Network blips or slow responses routinely cause duplicate deliveries, resulting in wallets being double-credited for a single bank transfer.

## How to Reproduce
Deliver the exact same `EVT-1001` credit event (`500_000` kobo) twice. In `buggy.py`, the balance becomes `1_000_000` kobo instead of `500_000`.

## Fix
Record each settled `event_id` (enforced with a `UNIQUE` constraint inside the same database transaction as the wallet credit in production) and safely ignore duplicates while returning HTTP 200.
