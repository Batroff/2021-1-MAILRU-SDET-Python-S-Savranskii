import logging
import shutil

from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--appium', default='http://127.0.0.1:4723/wd/hub')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    appium = request.config.getoption('--appium')
    debug_log = request.config.getoption('--debug_log')
    return {'appium': appium, 'debug_log': debug_log}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "skip_platform: skip test for necessary platform ",
    )

    base_test_dir = os.path.join('tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


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


@pytest.fixture(scope='session', autouse=True)
def add_allure_environment_property(request):
    allure_dir = request.config.getoption('--alluredir')
    if allure_dir:
        env_props = {
            'Appium': '1.20',
            'Android_emulator': '8.1',
        }

        if not os.path.exists(allure_dir):
            os.makedirs(allure_dir)
        allure_env_path = os.path.join(allure_dir, 'environment.properties')

        with open(allure_env_path, 'w') as f:
            for key, value in list(env_props.items()):
                f.write(f'{key}={value}\n')
