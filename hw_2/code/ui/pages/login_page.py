from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    url = 'https://account.my.com/login/'
    locators = LoginPageLocators()

    def __init__(self, driver):
        self.driver = driver
        assert self.is_opened(check_method=self._url_contains)

    def find_error(self):
        return self.find(self.locators.ERROR)
