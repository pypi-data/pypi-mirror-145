"""Component that emulates a Available Liquidity Ledger."""
from .ledger_base import LedgerBase


class AvailableLiquidityLedger(LedgerBase):
    """Component that emulates a Available Liquidity Ledger."""
    def __init__(self):
        super().__init__()
        self._ledger = {
            'LINK': {
                'block_num': [0],
                'funding_limit': [0],
                'BNT': [0],
                'LINK': [0]
            },
            'ETH': {
                'block_num': [0],
                'funding_limit': [0],
                'BNT': [0],
                'ETH': [0]
            },
            'wBTC': {
                'block_num': [0],
                'funding_limit': [0],
                'BNT': [0],
                'wBTC': [0]
            },
            'TKN': {
                'block_num': [0],
                'funding_limit': [0],
                'BNT': [0],
                'TKN': [0]
            },
            'BNT': {
                'block_num': [0],
                'funding_limit': [0],
                'BNT': [0]
            },
        }

