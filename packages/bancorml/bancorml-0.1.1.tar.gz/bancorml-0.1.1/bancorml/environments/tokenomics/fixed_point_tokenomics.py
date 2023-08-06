from bancorml.environments.tokenomics.tokenomics_base import TokenomicsBase


class FixedPointTokenomics(TokenomicsBase):
    """Tokenomics subclass for all fixed-point arithmetic.
    """

    MAX_UINT256 = 2 ** 256 - 1
    MAX_UINT128 = 2 ** 128 - 1

    def check_surplus(self, b, c, e, n, is_surplus=False, is_deficit=True, case='check surplus'):
        self.validate_signage_and_overflow(case)
        if (b + c) // (1 - n) > e: is_surplus, is_deficit = True, False
        self.surplus, self.deficit = is_surplus, is_deficit

    def check_hlim(self, b, c, e, x):
        self.validate_signage_and_overflow('check hlim')
        hlim = (c * e) // (b + c)
        satisfies_hlim = hlim > x
        self.hlim, self.satisfies_hlim = hlim, satisfies_hlim

    def check_hmax(self, b, c, e, m, n, x, is_surplus):
        if is_surplus:
            self.validate_signage_and_overflow('check hmax_surplus')
            hmax = b * e * (e * n + m * (b + c - e)) // ((1 - m) * (b + c - e) * (b + c - e * (1 - n)))
        else:
            self.validate_signage_and_overflow('check hmax_deficit')
            hmax = b * e * (e * n - m * (b + c - e * (1 - n))) // ((1 - m) * (b + c - e) * (b + c - e * (1 - n)))
        satisfies_hmax = hmax > x
        self.hmax, self.satisfies_hmax = hmax, satisfies_hmax

    def check_reduce_trading_liquidity(self, x, b, c, e, n, is_surplus, satisfies_hmax, satisfies_hlim,
                                       case='check reduce_trading_liquidity', reduce_trading_liquidity=False):
        if (satisfies_hmax == False) or (satisfies_hlim == False):
            self.validate_signage_and_overflow('check reduce_trading_liquidity')
            if is_surplus:
                reduce_trading_liquidity = x * (1 - n) > c
            else:
                reduce_trading_liquidity = (x * (1 - n) * (b + c)) // e > c
        self.reduce_trading_liquidity = reduce_trading_liquidity

    def handle_bootstrap_surplus(self, x, n):
        s = x * (1 - n)
        return s

    def handle_bootstrap_deficit_special_case(self, c, e, n, x):
        s = c * x * (1 - n) // e
        return s

    def handle_arbitrage_surplus(self, x, n, a, b, c, e, m):
        s = x * (1 - n)
        p = a * x * (b + c - e * (1 - n)) // ((1 - m) * (b * e + x * (b + c - e * (1 - n))))
        r = x * (b + c - e * (1 - n)) // e
        return p, r, s

    def handle_default_surplus(self, x, n, c, a, b):
        r = x * (0 - n) - c
        s = x * (0 - n)
        p = q = a * (x * (1 - n) - c) // b
        return p, q, r, s

    def handle_arbitrage_deficit(self, x, n, a, m, e, b, c):
        s = x * (1 - n)
        p = a * x * (1 - m) * (e * (1 - n) - b - c) // (b * e - x * (1 - m) * (e * (1 - n) - b - c))
        r = x * (e * (1 - n) - b - c) // e
        t = a * x * (1 - n) * (e - b - c) // (b * e)
        return p, r, s, t

    def handle_bootstrap_deficit(self, x, n, b, c, e, a):
        s = x * (1 - n) * (b + c) // e
        t = a * x * (1 - n) * (e - b - c) // (b * e)
        return s, t

    def handle_default_deficit(self, a, b, c, e, n, x):
        p = q = (a * (b * e - (b + c) * (e - x * (1 - n)))) // (b * e)
        r = (x * (1 - n) * (b + c) - c * e) // e
        s = (x * (1 - n) * (b + c)) // e
        t = (a * x * (1 - n) * (e - b - c)) // (b * e)
        return p, q, r, s, t

    def handle_external_wallet_adjustment_1(self, t, b, a):
        u = (t * b) // a
        t = 0
        return t, u

    def handle_external_wallet_adjustment_2(self, w, t, b, a):
        u = w
        t = (t * b - a * w) // b
        return t, u

    def validate_signage_and_overflow(self, case):
        for val, case in self.get_equations(self, case):
            assert 0 <= val, 'signage::{}'.format(case)
            assert val <= FixedPointTokenomics.MAX_UINT256, 'overflow::{}'.format(case)

    def get_equations(self, case):

        a, b, c, e, m, n, x, w, t = self.a, self.b, self.c, self.e, self.m, self.n, self.x, self.w, self.t

        if case == 'default deficit':
            equations = [(a * (b * e - (b + c) * (e - x * (1 - n))), f"{case} - 1"),
                         (b * e, f"{case} - 2"),
                         ((x * (1 - n) * (b + c) - c * e), f"{case} - 3"),
                         ((x * (1 - n) * (b + c)), f"{case} - 4"),
                         ((a * x * (1 - n) * (e - b - c)), f"{case} - 5")]

        elif case == 'bootstrap deficit':
            equations = [(x * (1 - n) * (b + c), f"{case} - 1"),
                         ((a * x * (1 - n) * (e - b - c)), f"{case} - 2"),
                         ((b * e), f"{case} - 3")]

        elif case == 'arbitrage deficit':
            equations = [(a * x * (1 - m) * (e * (1 - n) - b - c), f"{case} - 1"),
                         ((b * e - x * (1 - m) * (e * (1 - n) - b - c)), f"{case} - 2"),
                         (x * (e * (1 - n) - b - c), f"{case} - 3"),
                         (a * x * (1 - n) * (e - b - c), f"{case} - 4"),
                         (b * e, f"{case} - 5"),
                         (x * (1 - n), f"{case} - 6")]

        elif case == 'default surplus':
            equations = [(x * (0 - n) - c, f"{case} - 1"),
                         (x * (0 - n), f"{case} - 2"),
                         (a * (x * (1 - n) - c), f"{case} - 3")]

        elif case == 'bootstrap surplus':
            equations = [(x * (1 - n), f"{case} - 1")]

        elif case == 'arbitrage surplus':
            equations = [(x * (1 - n), f"{case} - 1"),
                         (a * x * (b + c - e * (1 - n)), f"{case} - 2"),
                         ((1 - m) * (b * e + x * (b + c - e * (1 - n))), f"{case} - 3"),
                         (x * (b + c - e * (1 - n)), f"{case} - 4"),
                         (e, f"{case} - 5")]

        elif case == 'bootstrap deficit (special case)':
            equations = [(c * x * (1 - n), f"{case} - 1")]

        elif case == 'bootstrap surplus (special case)':
            equations = [(x * (1 - n), f"{case} - 1")]

        elif case == 'external wallet adjustment (1)':
            equations = [(t * b, f"{case} - 1"),
                         (a, f"{case} - 2")]

        elif case == 'external wallet adjustment (2)':
            equations = [(t * b - a * w, f"{case} - 1"),
                         (b, f"{case} - 2")]

        elif case == 'check surplus':
            equations = [(b + c, f"{case} - 1"),
                         (1 - n, f"{case} - 2")]

        elif case == 'check hlim':
            equations = [(t * b - a * w, f"{case} - 1"),
                         (b, f"{case} - 2")]

        elif case == 'check hmax_surplus':
            equations = [(b * e * (e * n + m * (b + c - e)), f"{case} - 1"),
                         ((1 - m) * (b + c - e) * (b + c - e * (1 - n)), f"{case} - 2")]

        elif case == 'check hmax_deficit':
            equations = [(b * e * (e * n - m * (b + c - e * (1 - n))), f"{case} - 1"),
                         ((1 - m) * (b + c - e) * (b + c - e * (1 - n)), f"{case} - 2")]

        elif case == 'check reduce_trading_liquidity':
            equations = [(x * (1 - n), f"{case} - 1"),
                         (x * (1 - n) * (b + c), f"{case} - 2")]

        return equations
