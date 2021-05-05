import logging
import os
import shutil

import allure
import pytest

from api.ApiDashboard import ApiDashboard
from api.ApiSegment import ApiSegment
from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(config['url'])


@pytest.fixture(scope='function')
def api_dashboard(config):
    return ApiDashboard(config['url'])


@pytest.fixture(scope='function')
def api_segment(config):
    return ApiSegment(config['url'])


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    base_test_dir = os.path.join('tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')

    return {'url': url, 'browser': browser, 'debug_log': debug_log}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def test_dir(request):
    # filename.py-classname-test_name
    test_dir = os.path.join(request.config.base_test_dir, request._pyfuncitem.nodeid.replace('::', '-'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
