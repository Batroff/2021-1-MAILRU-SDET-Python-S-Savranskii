import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage


class BaseCase:

    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')

        if self.authorize:
            self.dashboard_page = request.getfixturevalue('login')

        self.logger.debug('Initial setup done!')

    def go_to_login_page(self):
        return LoginPage(driver=self.driver)
