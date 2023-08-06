from abc import ABC, abstractmethod
from decimal import *


class TokenomicsBase(ABC):
    """Tokenomics base class.

    TODO: Fill-in missing comments below
    """

    @property
    def surplus(self) -> bool:
        """
        """
        return self._surplus

    @surplus.setter
    def surplus(self, is_surplus: bool):
        """
        """
        self._surplus = is_surplus

    @property
    def deficit(self) -> bool:
        """
        """
        return self._deficit

    @deficit.setter
    def deficit(self, is_deficit: bool):
        """
        """
        self._deficit = is_deficit

    @property
    def hlim(self) -> int or Decimal:
        """
        """
        return self._hlim

    @hlim.setter
    def hlim(self, val: int or Decimal):
        """
        """
        self._hlim = val

    @property
    def satisfies_hlim(self) -> bool:
        """
        """
        return self._satisfies_hlim

    @satisfies_hlim.setter
    def satisfies_hlim(self, val: bool):
        """
        """
        self._satisfies_hlim = val

    @property
    def hmax(self) -> int or Decimal:
        """
        """
        return self._hmax

    @hmax.setter
    def hmax(self, val: int or Decimal):
        """
        """
        self._hmax = val

    @property
    def satisfies_hmax(self) -> bool:
        """
        """
        return self._satisfies_hmax

    @satisfies_hmax.setter
    def satisfies_hmax(self, val: bool):
        """
        """
        self._satisfies_hmax = val

    @property
    def reduce_trading_liquidity(self) -> bool:
        """
        """
        return self._reduce_trading_liquidity

    @reduce_trading_liquidity.setter
    def reduce_trading_liquidity(self, val: bool):
        """
        """
        self._reduce_trading_liquidity = val

    @abstractmethod
    def check_surplus(self, b, c, e, n, is_surplus=False, is_deficit=True, case='check surplus'):
        """
        """
        pass

    @abstractmethod
    def check_hmax(self, b, c, e, m, n, x, is_surplus):
        """
        """
        pass

    @abstractmethod
    def check_reduce_trading_liquidity(self, x, b, c, e, n, is_surplus, satisfies_hmax, satisfies_hlim, case='check reduce_trading_liquidity', reduce_trading_liquidity=False):
        """
        """
        pass

    @abstractmethod
    def handle_bootstrap_surplus(self, x, n):
        """
        """
        pass

    @abstractmethod
    def handle_bootstrap_deficit_special_case(self, c, e, n, x):
        """
        """
        pass

    @abstractmethod
    def handle_arbitrage_surplus(self, x, n, a, b, c, e, m):
        """
        """
        pass

    @abstractmethod
    def handle_default_surplus(self, x, n, c, a, b):
        """
        """
        pass

    @abstractmethod
    def handle_arbitrage_deficit(self, x, n, a, m, e, b, c):
        """
        """
        pass

    @abstractmethod
    def handle_bootstrap_deficit(self, x, n, b, c, e, a):
        """
        """
        pass

    @abstractmethod
    def handle_default_deficit(self, a, b, c, e, n, x):
        """
        """
        pass

    @abstractmethod
    def handle_external_wallet_adjustment_1(self, t, b, a):
        """
        """
        pass

    @abstractmethod
    def handle_external_wallet_adjustment_2(self, w, t, b, a):
        """
        """
        pass

    def check_external_wallet_adjustment(self, a, b, w, t, satisfies_hlim, satisfies_hmax, case=None):
        if ((satisfies_hlim == False) or (satisfies_hmax == False)) & (w > 0):
            if (a * w) > (t * b):
                case = 'external wallet adjustment (1)'
            else:
                case = 'external wallet adjustment (2)'
        return case





