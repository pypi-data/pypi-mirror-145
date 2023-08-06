from abc import ABC, abstractmethod

class AgentBase(ABC):
    """Base class for all agents."""

    @property
    @classmethod
    @abstractmethod
    def name(cls):
        """Returns string name of this component."""

