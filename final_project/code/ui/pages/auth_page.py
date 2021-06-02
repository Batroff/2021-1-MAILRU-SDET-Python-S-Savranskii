import allure

from ui.locators.pages_locators import AuthPageLocators
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from ui.pages.register_page import RegisterPage
from utils.decorators import wait


class AuthPage(BasePage):
    locators = AuthPageLocators()
    url = 'http://localhost:8080/' or 'http://localhost:8080/login'

    @allure.step('Login in...')
    def login(self, login, password, get_home_page=True):
        self.keys_to_input(self.locators.USERNAME_INPUT, login)
        self.keys_to_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.SUBMIT_BTN)

        if get_home_page:
            return HomePage(driver=self.driver)

    def is_login_error_exists(self, error_msg):
        def _check():
            locator = self.format_locator(self.locators.LOGIN_ERROR_TEMPLATE, error_msg)
            if self.element_exists(locator):
                return True

            raise TimeoutError(f'Login error with message "{error_msg}" doesn\'t exist.')

        return wait(method=_check, error=TimeoutError, timeout=10)

    def go_to_register_page(self) -> RegisterPage:
        self.click(self.locators.REGISTER_PAGE)
        return RegisterPage(driver=self.driver)
