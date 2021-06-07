import allure

from ui.locators.pages_locators import AuthPageLocators
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from ui.pages.register_page import RegisterPage


class AuthPage(BasePage):
    locators = AuthPageLocators()
    url = [f'http://{BasePage.host}:{BasePage.port}/',
           f'http://{BasePage.host}:{BasePage.port}/login']

    @allure.step('Login in...')
    def login(self, username, password, get_home_page=True):
        self.keys_to_input(self.locators.USERNAME_INPUT, username)
        self.keys_to_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.SUBMIT_BTN)

        if get_home_page:
            return HomePage(driver=self.driver)

    def is_error_exists(self, error_msg):
        return self.wait_text_in_element(locator=self.locators.LOGIN_ERROR, text=error_msg)

    def go_to_register_page(self) -> RegisterPage:
        self.click(self.locators.REGISTER_PAGE)
        return RegisterPage(driver=self.driver)
