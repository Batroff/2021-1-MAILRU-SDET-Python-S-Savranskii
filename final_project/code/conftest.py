import logging
import os
import shutil

import allure

from mysql.client import MysqlClient
from ui.fixtures import *


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='test_db')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_addoption(parser):
    parser.addoption('--url', default='http://localhost:8080')
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    base_test_dir = os.path.join('/tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

        mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='test_db')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_table('test_users')
        mysql_client.connection.close()

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')

    return {'url': url, 'debug_log': debug_log}


@pytest.fixture(scope='function')
def test_dir(request):
    test_dir = os.path.join(request.config.base_test_dir, request._pyfuncitem.nodeid.replace('::', '-'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


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
