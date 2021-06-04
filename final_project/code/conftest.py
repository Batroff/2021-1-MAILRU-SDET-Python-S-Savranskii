import logging
import shutil
from typing import Dict

from mysql.client import MysqlClient
from ui.fixtures import *
from utils.parser import parse_config


@pytest.fixture(scope='function')
def mysql_client():
    mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='test_db')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_addoption(parser):
    parser.addoption('--config', default='/app/app-config')
    parser.addoption('--selenoid', action='store_true', default=True)
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    base_test_dir = os.path.join('/tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        # Recreate test directories
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

        # Parse config file
        settings = parse_config(filepath=config.getoption('--config'))
        config.settings = settings

        # Recreate <name> database
        mysql_client = MysqlClient(user=settings['MYSQL_USER'],
                                   password=settings['MYSQL_PASSWORD'],
                                   db_name=settings['MYSQL_DB'])
        mysql_client.recreate_db()

        # Create table test_users
        mysql_client.connect()
        mysql_client.create_table(settings['MYSQL_TABLE'])
        mysql_client.connection.close()

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='session')
def config(request) -> Dict[str, str]:
    cfg = request.config.settings

    debug_log = request.config.getoption('--debug_log')
    selenoid = request.config.getoption('--selenoid')

    if selenoid:
        selenoid = 'http://localhost:4444/wd/hub'
        # selenoid = 'http://selenoid:4444/wd/hub'

    return dict({'selenoid': selenoid, 'debug_log': debug_log}, **cfg)


@pytest.fixture(scope='function')
def test_dir(request) -> str:
    test_dir = os.path.join(request.config.base_test_dir, request._pyfuncitem.nodeid.replace('::', '-'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def repo_root() -> str:
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'pytest.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('pytest')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
