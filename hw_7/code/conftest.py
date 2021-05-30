import copy
import logging
import os
import signal
import subprocess

from copy import copy
from mock import flask_mock

import pytest
import requests
from requests.exceptions import ConnectionError

import settings
from client.http_socket_client import HttpSocketClient
from utils.decorators import wait

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def http_socket_client():
    host = settings.APP_HOST
    port = int(settings.APP_PORT)

    return HttpSocketClient(host, port)


def _start_logs(log_name, dir_path='/tmp'):
    out_log = open(os.path.join(dir_path, log_name + '_out.log'), 'w')
    err_log = open(os.path.join(dir_path, log_name + '_err.log'), 'w')
    return out_log, err_log


def _start_proc(path, stdout, stderr, env):
    python_version = settings.PYTHON

    proc = subprocess.Popen([python_version, path], stdout=stdout, stderr=stderr, env=env)
    return proc


def start_app(config):
    app_path = os.path.join(repo_root, 'app', 'app.py')

    app_out, app_err = _start_logs('app')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_HOST
    env['APP_PORT'] = settings.APP_PORT

    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    env['MOCK_HOST'] = settings.MOCK_HOST
    env['MOCK_PORT'] = settings.MOCK_PORT

    proc = _start_proc(path=app_path, stdout=app_out, stderr=app_err, env=env)

    config.app_out = app_out
    config.app_err = app_err
    config.app_proc = proc

    def _check():
        requests.get(f'http://{settings.APP_HOST}:{settings.APP_PORT}')

    wait(method=_check, error=ConnectionError)


def stop_app(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def start_stub(config):
    stub_path = os.path.join(repo_root, 'stub', 'flask_stub.py')

    stub_out, stub_err = _start_logs('stub')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT
    proc = _start_proc(path=stub_path, stdout=stub_out, stderr=stub_err, env=env)

    config.stub_out = stub_out
    config.stub_err = stub_err
    config.stub_proc = proc

    def _check():
        requests.get(f'http://{settings.STUB_HOST}:{settings.STUB_PORT}')

    wait(method=_check, error=ConnectionError)


def stop_stub(config):
    config.stub_proc.send_signal(signal.SIGINT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def start_mock():
    flask_mock.run_mock()

    def _check():
        requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}')

    wait(method=_check, error=ConnectionError)


def stop_mock():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock()
        start_stub(config)
        start_app(config)


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock()


@pytest.fixture(scope='function', autouse=True)
def requests_logger():
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s'
                                      '\n-------------------')
    log_file = os.path.join('/tmp', 'requests.log')

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setLevel('INFO')
    file_handler.setFormatter(log_formatter)

    log = logging.getLogger('requests')
    log.propagate = False
    log.setLevel('INFO')
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
