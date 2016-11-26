import pytest
import os.path
import json
from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        target_filename = file
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), target_filename) \
            if os.path.basename(target_filename) == target_filename else target_filename
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    config = load_config(request.config.getoption("--target"))
    if fixture is None:
        fixture = Application(app_path=config['app_path'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--target", action="store", default="target.json")