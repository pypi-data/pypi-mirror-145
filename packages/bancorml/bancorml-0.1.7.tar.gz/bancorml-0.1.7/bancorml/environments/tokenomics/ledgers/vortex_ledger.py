"""Component that emulates a Vortex Ledger Ledger."""
from .ledger_base import LedgerBase

class VortexLedger(LedgerBase):
    """Component that emulates a Vortex Ledger Ledger."""
    def __init__(self):
        super().__init__()
        self._ledger = {'block_num': [0], 'BNT':[0]}


