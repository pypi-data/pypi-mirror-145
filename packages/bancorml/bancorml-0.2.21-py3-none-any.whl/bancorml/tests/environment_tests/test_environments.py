import unittest
import pytest
from bancorml.utils import parse_json_tests, load_test_data
from bancorml.environments import Bancor3
from bancorml.utils.schemas import FloatingPointUnstakeTKN

PRECISION = 10
IS_SOLIDITY = False
protocol = Bancor3(is_solidity=IS_SOLIDITY)

@pytest.mark.usefixtures("protocol")
class TestWithdrawalAlgorithm(unittest.TestCase):

    def test_check_surplus(self):
        X = load_test_data()
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            t_is_surplus = True if X['is_tkn_surplus'].values[indx]=='True' else False
            protocol = Bancor3(is_solidity=IS_SOLIDITY)
            protocol.tokenomics.check_surplus(b, c, e, n)
            is_surplus, is_deficit = protocol.tokenomics.surplus, protocol.tokenomics.deficit
            assert is_surplus == t_is_surplus, f"is_surplus={is_surplus} != t_is_surplus={t_is_surplus} on index={indx}"

    def test_hlim(self):
        X = load_test_data()
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            t_satisfies_hlim = True if X['satisfies_hlim'].values[indx]=='True' else False
            protocol.tokenomics.check_hlim(b, c, e, x)
            satisfies_hlim = protocol.tokenomics.satisfies_hlim
            assert satisfies_hlim == t_satisfies_hlim, f"test_hlim failed on index={indx}"

    def test_hmax_deficit(self):
        X = load_test_data()
        X = X[(X['is_tkn_surplus'] == 'False') & (X['x'].astype(float) > 0)]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            t_satisfies_hmax = True if X['satisfies_hmax'].values[indx]=='True' else False
            protocol.tokenomics.check_hmax(b, c, e, m, n, x, False)
            satisfies_hmax  = protocol.tokenomics.satisfies_hmax
            assert satisfies_hmax == t_satisfies_hmax, f"test_hmax_deficit failed on index={indx}"

    def test_hmax_surplus(self):
        X = load_test_data()
        X = X[(X['is_tkn_surplus'] == 'True') & (X['x'].astype(float) > 0)]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            t_satisfies_hmax = True if X['satisfies_hmax'].values[indx] == 'True' else False
            protocol.tokenomics.check_hmax(b, c, e, m, n, x, True)
            satisfies_hmax = protocol.tokenomics.satisfies_hmax
            assert satisfies_hmax == t_satisfies_hmax, f"test_hmax_surplus failed on index={indx}"

    def test_reduce_trading_liquidity(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            satisfies_hmax = True if X['satisfies_hmax'].values[indx] == 'True' else False
            is_surplus = True if X['is_tkn_surplus'].values[indx] == 'True' else False
            satisfies_hlim = True if X['satisfies_hlim'].values[indx] == 'True' else False
            require_reduce_trading_liquidity = True if X['require_reduce_trading_liquidity'].values[indx] == 'True' else False
            protocol.tokenomics.check_reduce_trading_liquidity(x, b, c, e, n, is_surplus, satisfies_hmax, satisfies_hlim)
            reduce_trading_liquidity = protocol.tokenomics.reduce_trading_liquidity
            assert reduce_trading_liquidity == require_reduce_trading_liquidity, f"test_reduce_trading_liquidity failed on index={indx}"

    def test_p(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(p) and 'E' not in str(_p):
                p = str(p).split('.')[0] + '.' + str(p).split('.')[-1][:PRECISION]
                _p = str(_p).split('.')[0] + '.' + str(_p).split('.')[-1][:PRECISION]
                assert p == _p, f"test_p failed on index={indx}, case={case}"

    def test_q(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(q) and 'E' not in str(_q):
                q = str(q).split('.')[0] + '.' + str(q).split('.')[-1][:PRECISION]
                _q = str(_p).split('.')[0] + '.' + str(_q).split('.')[-1][:PRECISION]
                assert q == _q, f"test_q failed on index={indx}, case={case}"

    def test_r(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(r) and 'E' not in str(_r):
                r = str(r).split('.')[0] + '.' + str(r).split('.')[-1][:PRECISION]
                _r = str(_r).split('.')[0] + '.' + str(_r).split('.')[-1][:PRECISION]
                assert r == _r, f"test_q failed on index={indx}, case={case}"

    def test_s(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(s) and 'E' not in str(_s):
                s = str(s).split('.')[0] + '.' + str(s).split('.')[-1][:PRECISION]
                _s = str(_s).split('.')[0] + '.' + str(_s).split('.')[-1][:PRECISION]
                assert s == _s, f"test_q failed on index={indx}, case={case}"

    def test_t(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(t) and 'E' not in str(_t):
                t = str(t).split('.')[0] + '.' + str(t).split('.')[-1][:PRECISION]
                _t = str(_t).split('.')[0] + '.' + str(_t).split('.')[-1][:PRECISION]
                assert t == _t, f"test_t failed on index={indx}, case={case}"

    def test_u(self):
        X = load_test_data()
        X = X[X['x'].astype(float) > 0]
        for indx in range(len(X)):
            a, b, c, e, n, x, w, m, _p, _q, _r, _s, _t, _u = parse_json_tests(X, indx)
            input_params = dict(
                a=a,
                b=b,
                e=e,
                w=w,
                c=c,
                n=n,
                m=m,
                x=x
            )
            params = FloatingPointUnstakeTKN(**input_params)
            case, p, q, r, s, t, u = protocol.get_state(params)
            if 'E' not in str(u) and 'E' not in str(_u):
                u = str(u).split('.')[0] + '.' + str(u).split('.')[-1][:PRECISION]
                _u = str(_u).split('.')[0] + '.' + str(_u).split('.')[-1][:PRECISION]
                assert u == _u, f"test_u failed on index={indx}, case={case}"
