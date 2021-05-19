import pytest

from client.http_socket_client import HttpSocketClient


class BaseCase(object):

    http_client = None
    logger = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: pytest.FixtureRequest, requests_logger):
        self.http_client: HttpSocketClient = request.getfixturevalue('http_socket_client')
        self.logger = requests_logger
