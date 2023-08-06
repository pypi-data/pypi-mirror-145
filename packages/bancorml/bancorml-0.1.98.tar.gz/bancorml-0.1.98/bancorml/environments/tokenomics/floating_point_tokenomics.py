from bancorml.environments.tokenomics.tokenomics_base import TokenomicsBase
from decimal import *

class FloatingPointTokenomics(TokenomicsBase):
    """Tokenomics subclass for all floating-point arithmetic.
    """

    def check_surplus(self, b, c, e, n, is_surplus=False, is_deficit=True, case='check surplus'):
        if (b + c) / (1 - n) > e: is_surplus, is_deficit = True, False
        self.surplus, self.deficit = is_surplus, is_deficit

    def check_hlim(self, b, c, e, x):
        hlim = (c * e) / (b + c)
        satisfies_hlim = hlim > x
        self.hlim, self.satisfies_hlim = hlim, satisfies_hlim

    def check_hmax(self, b, c, e, m, n, x, is_surplus):

        if is_surplus:
            hmax = b * e * (e * n + m * (b + c - e)) / ((1 - m) * (b + c - e) * (b + c - e * (1 - n)))
        else:
            hmax = b * e * (e * n + m * (e * (1 - n) - b - c)) / ((1 - m) * (e - b - c) * (e * (1 - n) - b - c))

        satisfies_hmax = hmax > x
        self.hmax, self.satisfies_hmax = hmax, satisfies_hmax

    def check_reduce_trading_liquidity(self, x, b, c, e, n, is_surplus, satisfies_hmax, satisfies_hlim,
                                       case='check reduce_trading_liquidity', reduce_trading_liquidity=False):
        if (satisfies_hmax == False) or (satisfies_hlim == False):
            reduce_trading_liquidity = (x * (1 - n)) <= c if is_surplus else ((x * (1 - n) * (b + c)) / e) <= c
        self.reduce_trading_liquidity = reduce_trading_liquidity

    def handle_bootstrap_surplus(self, x, n):
        s = x * (1 - n)
        return s

    def handle_bootstrap_deficit_special_case(self, c, e, n, x):
        s = c * x * (1 - n) / e
        return s

    def handle_arbitrage_surplus(self, x, n, a, b, c, e, m):
        s = x * (1 - n)
        p = a * x * (b + c - e * (1 - n)) / ((1 - m) * (b * e + x * (b + c - e * (1 - n))))
        r = x * (b + c - e * (1 - n)) / e
        return p, r, s

    def handle_default_surplus(self, x, n, c, a, b):
        r = x * (1 - n) - c
        s = x * (1 - n)
        p = q = a * (x * (1 - n) - c) / b
        return p, q, r, s

    # def handle_default_surplus(self, x, n):
    #     s = x * (1 - n)
    #     return s

    def handle_arbitrage_deficit(self, x, n, a, m, e, b, c):
        s = x * (1 - n)
        p = a * x * (1 - m) * (e * (1 - n) - b - c) / (b * e - x * (1 - m) * (e * (1 - n) - b - c))
        r = x * (e * (1 - n) - b - c) / e
        # t = a * x * (1 - n) * (e - b - c) / (b * e)
        return p, r, s

    def handle_bootstrap_deficit(self, x, n, b, c, e, a):
        s = x * (1 - n) * (b + c) / e
        t = a * x * (1 - n) * (e - b - c) / (b * e)
        return s, t

    def handle_default_deficit(self, a, b, c, e, n, x):
        p = q = (a * (b * e - (b + c) * (e - x * (1 - n)))) / (b * e)
        r = (x * (1 - n) * (b + c) - c * e) / e
        s = (x * (1 - n) * (b + c)) / e
        t = (a * x * (1 - n) * (e - b - c)) / (b * e)
        return p, q, r, s, t

    def handle_external_wallet_adjustment_1(self, t, b, a):
        u = (t * b) / a
        t = 0
        return t, u

    def handle_external_wallet_adjustment_2(self, w, t, b, a):
        u = w
        t = (t * b - a * w) / b
        return t, u

    def handle_trade_bnt_to_tkn(self, a, d, b, x, e):
        bnt_trading_liquidity = (a * (a + x) + d * (1 - e) * (a * x + x * x)) / (a + d * x)
        tkn_trading_liquidity = (b * (a + d * x)) / (a + x)
        tkn_out = (b * x * (1 - d)) / (a + x)
        tkn_fee = (b * d * x * (1 - e)) / (a + x)
        vortex_fee = (d * e * x * (a + x)) / (a + d * x)
        return bnt_trading_liquidity, tkn_trading_liquidity, tkn_out, tkn_fee, vortex_fee

    def handle_trade_tkn_to_bnt(self, a, d, b, x, e):
        bnt_trading_liquidity = (a * (b + d * x * (1 - e))) / (b + x)
        tkn_trading_liquidity = b + x
        bnt_out = (a * x * (1 - d)) / (b + x)
        bnt_fee = (a * d * x * (1 - e)) / (b + x)
        vortex_fee = (a * d * e * x) / (b + x)
        return bnt_trading_liquidity, tkn_trading_liquidity, bnt_out, bnt_fee, vortex_fee

    def handle_trade_tkn_to_tkn(self, a1, d1, b1, a2, d2, b2, x, e):
        bnt_source_trading_liquidity = (a1 * (b1 + d1 * x * (1 - e))) / (b1 + x)
        tkn_source_trading_liquidity = b1 + x
        bnt_destination_trading_liquidity = ((a1 * x * (1 - d1) + a2 * (b1 + x)) * (a1 * d2 * x * (1 - d1) * (1 - e) + a2 * (b1 + x))) / ((b1 + x) * (a1 * d2 * x * (1 - d1) + a2 * (b1 + x)))
        tkn_destination_trading_liquidity = (b2 * (a1 * d2 * x * (1 - d1) + a2 * (b1 + x))) / (a1 * x * (1 - d1) + a2 * (b1 + x))
        tkn_out = (a1 * b2 * x * (1 - d1) * (1 - d2)) / (a1 * x * (1 - d1) + a2 * (b1 + x))
        bnt_fee = (a1 * d1 * x * (1 - e)) / (b1 + x)
        tkn_fee = (a1 * b2 * d2 * x * (1 - d1) * (1 - e)) / (a1 * x * (1 - d1) + a2 * (b1 + x))
        vortex_fee = (a1 * e * x * (a1 * d2 * x * (1 - d1) + a2 * (b1 + x) * (d1 + d2 - d1 * d2))) / ((b1 + x) * (a1 * d2 * x * (1 - d1) + a2 * (b1 + x)))
        return bnt_source_trading_liquidity, tkn_source_trading_liquidity, bnt_destination_trading_liquidity, tkn_destination_trading_liquidity, tkn_out, bnt_fee, tkn_fee, vortex_fee


