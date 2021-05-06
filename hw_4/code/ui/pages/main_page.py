from ui.locators.locators_android import MainPageLocators
from ui.pages.base_page import BasePage
from ui.pages.chat_page import ChatPage
from ui.pages.settings_page import SettingsPage


class MainPage(BasePage):
    locators = MainPageLocators()

    def go_to_chat_page(self):
        self.click(self.locators.OPEN_CHAT)
        return ChatPage(driver=self.driver)

    def go_to_settings_page(self):
        self.click(self.locators.OPEN_SETTINGS)
        return SettingsPage(driver=self.driver)
