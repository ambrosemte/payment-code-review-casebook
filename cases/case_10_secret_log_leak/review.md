# Case 10: Leaking Secrets and Transaction PINs in Error Logs

- **Severity:** High
- **Category:** Secrets Management & Observability

## What Is Wrong
`format_error_log_buggy()` serializes the entire raw request payload into error logs without redacting sensitive fields (`pin`, `api_secret`, `token`, `otp`).

## Why It Matters
Application logs are frequently shipped to third-party log aggregators, Slack alerts, or support dashboards with broader access than production databases. Exposing transaction PINs or API secrets enables account takeover and violates PCI/data-protection standards.

## How to Reproduce
Pass a payload containing `"pin": "4821"` and `"api_secret": "sk_test_example_999"` to `format_error_log_buggy()`. Both raw values appear in plaintext in the returned log string.

## Fix
Recursively redact sensitive keys (`pin`, `password`, `otp`, `token`, `api_secret`, `authorization`) before serializing any request context into logs.
