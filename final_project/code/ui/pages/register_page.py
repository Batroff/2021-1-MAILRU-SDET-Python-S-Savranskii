import os
import random

from api.vk_client import VkApiClient
from ui.locators.pages_locators import RegisterPageLocators
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage


class RegisterPage(BasePage):
    locators = RegisterPageLocators()

    url = [f'http://{BasePage.host}:{BasePage.port}/reg']

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

    def is_error_exists(self, error_msg):
        return self.wait_text_in_element(locator=self.locators.REGISTER_ERROR, text=error_msg)
