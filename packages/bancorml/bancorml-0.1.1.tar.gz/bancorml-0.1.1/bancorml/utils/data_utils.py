"""Load the datasets"""
import pandas as pd
from decimal import *
import os

def decimal_from_value(value):
    return Decimal(value)

def parse_json_tests(X, indx):
    a = Decimal(X['a'].values[indx])
    b = Decimal(X['b'].values[indx])
    c = Decimal(X['c'].values[indx])
    e = Decimal(X['e'].values[indx])
    n = Decimal(X['n'].values[indx])
    x = Decimal(X['x'].values[indx])
    w = Decimal(X['w'].values[indx])
    m = Decimal(X['m'].values[indx])
    p = Decimal(X['P'].values[indx])
    q = Decimal(X['Q'].values[indx])
    r = Decimal(X['R'].values[indx])
    s = Decimal(X['S'].values[indx])
    t = Decimal(X['T'].values[indx])
    u = Decimal(X['U'].values[indx])
    return a, b, c, e, n, x, w, m, p, q, r, s, t, u

converters={'a': str,
           'b': str,
           'c': str,
           'e': str,
           'm': str,
           'n': str,
           'w': str,
           'x': str,
           'is_tkn_surplus': str,
           'hlim': str,
           'satisfies_hlim': str,
           'hmax': str,
           'satisfies_hmax': str,
           'require_reduce_trading_liquidity': str,
           'P': str,
           'Q': str,
           'P': str,
           'Q': str,
           'R': str,
           'S': str,
           'T': str,
           'U': str,
}

def load_test_data():
    data_path = os.path.join(os.path.dirname(__file__), "data/withdrawal_algorithm_tests.json")
    data_path = data_path.replace('utils', 'tests/environment_tests')
    return pd.read_json(data_path, dtype=converters)

def load_data(path='data/MBRtest1.json', filetype='json', index=None, target=None, n_rows=None, drop=None, verbose=True, **kwargs):
    """Load features and target from file.

    Args:
        path (str): Path to file or a http/ftp/s3 URL.
        index (str): Column for index.
        target (str): Column for target.
        n_rows (int): Number of rows to return. Defaults to None.
        drop (list): List of columns to drop. Defaults to None.
        verbose (bool): If True, prints information about features and target. Defaults to True.
        **kwargs: Other keyword arguments that should be passed to panda's `read_csv` method.

    Returns:
        pd.DataFrame, pd.Series: Features matrix and target.
    """
    if filetype=='csv':
        feature_matrix = pd.read_csv(path, index_col=index, nrows=n_rows, dtype=converters, **kwargs)
    elif filetype=='json':
        feature_matrix = pd.read_json(path, index_col=index, nrows=n_rows, dtype=converters, **kwargs)

    if target is not None:
        targets = [target] + (drop or [])
        y = feature_matrix[target]
        X = feature_matrix.drop(columns=targets)
    else:
        X = feature_matrix

    if verbose:
        # number of features
        print(len(X.columns), end="\n\n")

        # number of total training examples
        info = "Number of training examples: {}"
        print(info.format(len(X)), end="\n")

    try: return X, y
    except: return X
