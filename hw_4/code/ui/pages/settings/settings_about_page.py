from ui.locators.locators_android import SettingsAboutPageLocators
from ui.pages.base_page import BasePage


class SettingsAboutPage(BasePage):
    locators = SettingsAboutPageLocators()

    def get_about_program(self):
        version = self.find(self.locators.ABOUT_PROGRAM_VERSION).text
        trademark = self.find(self.locators.ABOUT_PROGRAM_TRADEMARK).text

        return version, trademark
