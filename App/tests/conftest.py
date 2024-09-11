import pytest
from devloapp import app



app.which = "devlotest"


print("Chargement de conftest...")

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--runslow")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)