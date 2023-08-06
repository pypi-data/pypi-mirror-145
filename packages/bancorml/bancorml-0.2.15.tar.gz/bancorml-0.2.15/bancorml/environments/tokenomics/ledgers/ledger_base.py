"""Base class for all ledgers."""
from abc import ABC, abstractmethod

class LedgerBase(ABC):
    """Base class for all ledgers."""

    def _validate_ledger(self, ledger, new_state):
        if not isinstance(new_state, ledger):
            raise ValueError(
                f"Invalid type {new_state}. New state must be an instance of {ledger}"
            )

    @property
    def ledger(self):
        """
        Returns:
            (dict): Dictionary representing the ledger balance
        """
        return self._ledger

    @ledger.setter
    def ledger(self, new_state):
        """
        Args:
            new_state (dict): Dictionary representing the new state of the ledger balance

        Returns:
            (dict): Dictionary representing the updated ledger balance
        """
        self._validate_balance(type(self.ledger), new_state)
        self._ledger = new_state