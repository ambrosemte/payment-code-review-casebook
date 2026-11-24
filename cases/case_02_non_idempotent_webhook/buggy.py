"""Case 02 (Buggy): Non-idempotent payment webhook handler."""


class BuggyWebhookProcessor:
    def __init__(self):
        self.balances: dict[str, int] = {}

    def handle_credit_event(self, event: dict) -> dict:
        # BUG: Never records or checks event_id; retried webhooks credit twice.
        user_id = event["user_id"]
        amount = int(event["amount_kobo"])
        self.balances[user_id] = self.balances.get(user_id, 0) + amount
        return {"status": "credited", "balance": self.balances[user_id]}
