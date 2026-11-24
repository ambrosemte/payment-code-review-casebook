"""Case 01 (Buggy): Wallet debit check-then-act race condition."""

import time


class BuggyWallet:
    def __init__(self, balance: int):
        self.balance = balance

    def debit(self, amount: int) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        # BUG: Unsynchronized read-check-write window allows concurrent overdraft.
        current = self.balance
        if current < amount:
            return False
        time.sleep(0.02)  # Simulates I/O or DB latency before write
        self.balance = current - amount
        return True
