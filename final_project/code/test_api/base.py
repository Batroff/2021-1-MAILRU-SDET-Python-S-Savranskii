import pytest

from mysql.builder import MySQLBuilder


class ApiBaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger, app_api_client, mysql_client):
        self.logger = logger
        self.app_api_client = app_api_client

        self.mysql_client = mysql_client
        self.mysql_builder = MySQLBuilder(self.mysql_client)

        self.prepare()

    def prepare(self):
        pass
