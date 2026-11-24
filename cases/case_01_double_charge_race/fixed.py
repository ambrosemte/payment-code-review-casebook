"""Case 01 (Fixed): Synchronized wallet debit preventing concurrent double-spend."""

import threading
import time


class FixedWallet:
    def __init__(self, balance: int):
        self.balance = balance
        self._lock = threading.Lock()

    def debit(self, amount: int) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        with self._lock:
            if self.balance < amount:
                return False
            time.sleep(0.02)
            self.balance -= amount
            return True
