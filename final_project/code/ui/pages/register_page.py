from ui.locators.pages_locators import RegisterPageLocators
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from utils.decorators import wait


class RegisterPage(BasePage):
    locators = RegisterPageLocators()
    url = 'http://localhost:8080/reg'

    def register(self, username, email, password, confirm_password, checkbox, get_home_page=True):
        self.keys_to_input(self.locators.USERNAME_INPUT, username)
        self.keys_to_input(self.locators.EMAIL_INPUT, email)
        self.keys_to_input(self.locators.PASSWORD_INPUT, password)
        self.keys_to_input(self.locators.PASSWORD_CONFIRM_INPUT, confirm_password)

        if checkbox:
            self.find(self.locators.CHECKBOX_INPUT).click()

        self.click(self.locators.SUBMIT_BTN)

        if get_home_page:
            return HomePage(driver=self.driver)

    def is_reg_error_exists(self, error_msg):
        def _check():
            locator = self.format_locator(self.locators.REGISTER_ERROR_TEMPLATE, error_msg)
            if self.element_exists(locator):
                return True

            raise TimeoutError(f'Registration error with message "{error_msg}" doesn\'t exist.')

        return wait(method=_check, error=TimeoutError, timeout=10)
