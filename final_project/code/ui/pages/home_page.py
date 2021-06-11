import logging

import allure

from ui.locators.pages_locators import HomePageLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('pytest')


class HomePage(BasePage):
    url = [f'http://{BasePage.host}:{BasePage.port}/welcome/']
    locators = HomePageLocators()

    @allure.step('Returning to home page')
    def go_to_home_page(self):
        self.click(self.format_locator(self.locators.MENU_LINK_TEMPLATE, 'HOME'))

        return HomePage(driver=self.driver)

    @allure.step('Click on menu link with "{name}" title')
    def go_to_linked_page(self, name):
        locator = self.format_locator(self.locators.MENU_LINK_TEMPLATE, name)
        self.click(locator)

    def get_link_target(self, link_text):
        locator = self.format_locator(self.locators.MENU_LINK_TEMPLATE, link_text)
        element = self.find(locator)

        logging.debug(f'Locator = "{locator}", attribute = "{element.get_attribute("target")}"')
        return element.get_attribute('target')

    @allure.step('Click on dropdown menu link with "{header_name}" header; "{dropdown_name}" link name')
    def go_to_dropdown_linked_page(self, header_name, dropdown_name):
        header = self.format_locator(self.locators.MENU_LINK_TEMPLATE, header_name)
        name = self.format_locator(self.locators.MENU_LINK_TEMPLATE, dropdown_name)

        self.action_chains \
            .move_to_element(self.find(header)) \
            .pause(0.1) \
            .click(self.find(name)) \
            .perform()

    @allure.step('Switching to next tab')
    def switch_to_next_tab(self, current_window_handler):
        for handler in self.driver.window_handles:
            if handler != current_window_handler:
                self.driver.close()
                self.driver.switch_to.window(handler)
                return

    def get_username(self):
        element = self.find(self.locators.MENU_USERNAME)
        return element.text.split(' as ')[-1]

    def get_vk_id(self):
        element = self.find(self.locators.MENU_VK_ID)
        return element.text.split(': ')[-1]

    def logout(self):
        self.click(self.locators.MENU_LOGOUT)

    def go_to_image_linked_page(self, name):
        locator = self.format_locator(self.locators.IMAGE_LINK_BY_TITLE_TEMPLATE, name)
        self.click(locator)
