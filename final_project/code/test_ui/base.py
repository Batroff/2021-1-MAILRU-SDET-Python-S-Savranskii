import os
import random

import pytest
from _pytest.fixtures import FixtureRequest

from mysql.builder import MySQLBuilder
from ui.pages.home_page import HomePage


class BaseCase:
    driver = None
    config = None
    logger = None

    authorize = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest, ui_report):

        self.driver = driver
        self.config = config
        self.logger = logger

        self.mysql_client = request.getfixturevalue('mysql_client')
        self.mysql_builder = MySQLBuilder(self.mysql_client)

        self.vk_api_client = request.getfixturevalue('vk_api_client')

        self.auth_page = request.getfixturevalue('auth_page')

        if self.authorize:
            user = self.mysql_builder.create_user()
            os.environ['USER_USERNAME'] = user.username
            os.environ['USER_PASSWORD'] = user.password

            vk_id = str(random.randint(1000, 10000))
            self.vk_api_client.add_vk_id(username=user.username, vk_id=vk_id)

            self.home_page: HomePage = self.auth_page.login(username=user.username, password=user.password)

        self.prepare()

    def prepare(self):
        pass
