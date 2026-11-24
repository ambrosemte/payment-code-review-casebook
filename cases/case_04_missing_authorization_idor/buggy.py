"""Case 04 (Buggy): Missing object-level authorization check (IDOR / BOLA)."""


class BuggyReceiptService:
    def __init__(self, receipts: dict[str, dict]):
        self._receipts = receipts

    def get_receipt(self, requester_user_id: str, receipt_id: str) -> dict:
        # BUG: Looks up receipt by ID without verifying ownership by requester_user_id.
        receipt = self._receipts.get(receipt_id)
        if not receipt:
            raise KeyError("Receipt not found")
        return receipt
