"""Component that emulates a Staking Ledger."""
from .ledger_base import LedgerBase

class StakingLedger(LedgerBase):
    def __init__(self):
        super().__init__()
        self._ledger = {'block_num': [0]}
