"""Case 02 (Fixed): Idempotent payment webhook handler."""


class FixedWebhookProcessor:
    def __init__(self):
        self.balances: dict[str, int] = {}
        self._processed_events: set[str] = set()

    def handle_credit_event(self, event: dict) -> dict:
        event_id = event["event_id"]
        user_id = event["user_id"]
        if event_id in self._processed_events:
            return {"status": "duplicate_ignored", "balance": self.balances.get(user_id, 0)}

        amount = int(event["amount_kobo"])
        self.balances[user_id] = self.balances.get(user_id, 0) + amount
        self._processed_events.add(event_id)
        return {"status": "credited", "balance": self.balances[user_id]}
