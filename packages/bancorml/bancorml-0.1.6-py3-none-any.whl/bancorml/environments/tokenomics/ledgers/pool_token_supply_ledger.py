"""Component that emulates a Liquidity Pool Ledger."""
from .ledger_base import LedgerBase

class PoolTokenSupplyLedger(LedgerBase):
    def __init__(self):
        super().__init__()
        self._ledger = {}

