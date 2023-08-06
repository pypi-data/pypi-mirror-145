import sys
import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "skip_offline: mark test to be skipped if offline (https://api.featurelabs.com cannot be reached)",
    )
    config.addinivalue_line(
        "markers", "noncore_dependency: mark test as needing non-core dependencies"
    )
    config.addinivalue_line(
        "markers",
        "skip_during_conda: mark test to be skipped if running during conda build",
    )
    config.addinivalue_line(
        "markers",
        "skip_if_39: mark test to be skipped if running during conda build",
    )


@pytest.fixture(scope="session")
def go():
    from plotly import graph_objects as go

    return go


@pytest.fixture(scope="session")
def im():
    from imblearn import over_sampling as im

    return im


@pytest.fixture(scope="session")
def graphviz():
    import graphviz

    return graphviz


def pytest_addoption(parser):
    parser.addoption(
        "--has-minimal-dependencies",
        action="store_true",
        default=False,
        help="If true, tests will assume only the dependencies in"
        "core-requirements.txt have been installed.",
    )
    parser.addoption(
        "--is-using-conda",
        action="store_true",
        default=False,
        help="If true, tests will assume that they are being run as part of"
        "the build_conda_pkg workflow with the feedstock.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--has-minimal-dependencies"):
        skip_noncore = pytest.mark.skip(reason="needs noncore dependency")
        for item in items:
            if "noncore_dependency" in item.keywords:
                item.add_marker(skip_noncore)
    if config.getoption("--is-using-conda"):
        skip_conda = pytest.mark.skip(reason="Test does not run during conda")
        for item in items:
            if "skip_during_conda" in item.keywords:
                item.add_marker(skip_conda)
    if sys.version_info >= (3, 9):
        skip_39 = pytest.mark.skip(reason="Test dependency not supported in python 3.9")
        for item in items:
            if "skip_if_39" in item.keywords:
                item.add_marker(skip_39)


@pytest.fixture
def has_minimal_dependencies(pytestconfig):
    return pytestconfig.getoption("--has-minimal-dependencies")


@pytest.fixture
def is_using_conda(pytestconfig):
    return pytestconfig.getoption("--is-using-conda")


@pytest.fixture
def is_using_windows(pytestconfig):
    return sys.platform in ["win32", "cygwin"]


@pytest.fixture
def is_running_py_39_or_above():
    return sys.version_info >= (3, 9)


@pytest.fixture
def protocol():
    from bancorml.environments import Bancor3
    protocol = Bancor3
    return protocol


