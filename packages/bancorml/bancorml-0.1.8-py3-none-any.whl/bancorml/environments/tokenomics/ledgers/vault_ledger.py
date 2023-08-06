"""Component that emulates a Vault Ledger."""
from .ledger_base import LedgerBase

class VaultLedger(LedgerBase):
    """Component that emulates a Vault Ledger."""
    def __init__(self):
        super().__init__()
        self._ledger = {'block_num': [0]}
