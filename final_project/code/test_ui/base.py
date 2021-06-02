import pytest
from _pytest.fixtures import FixtureRequest
from selenium import webdriver

from mysql.builder import MySQLBuilder
from mysql.client import MysqlClient
from ui.pages.auth_page import AuthPage


class BaseCase:
    driver = None
    config = None
    logger = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver: webdriver = driver
        self.config = config
        self.logger = logger

        self.mysql: MysqlClient = request.getfixturevalue('mysql_client')
        self.mysql_builder = MySQLBuilder(self.mysql)

        self.auth_page: AuthPage = request.getfixturevalue('auth_page')

        self.prepare()

    def prepare(self):
        pass
