"""Case 04 (Fixed): Scoped object-level authorization check."""


class FixedReceiptService:
    def __init__(self, receipts: dict[str, dict]):
        self._receipts = receipts

    def get_receipt(self, requester_user_id: str, receipt_id: str) -> dict:
        receipt = self._receipts.get(receipt_id)
        if not receipt or receipt["owner_id"] != requester_user_id:
            raise PermissionError("Access denied or receipt not found")
        return receipt
