from ui.locators.locators_android import SettingsPageLocators
from ui.pages.base_page import BasePage
from ui.pages.settings.settings_about_page import SettingsAboutPage
from ui.pages.settings.settings_source_page import SettingsSourcePage


class SettingsPage(BasePage):
    locators = SettingsPageLocators()

    def go_to_source_page(self):
        source_menu_btn = self.locators.FEED_SOURCE_MENU
        self.swipe_to_element(swipe_method=self.swipe_up, locator=source_menu_btn, max_swipes=5)
        self.click(source_menu_btn)
        return SettingsSourcePage(driver=self.driver)

    def go_to_about_page(self):
        about_menu_btn = self.locators.ABOUT_MENU
        self.swipe_to_element(swipe_method=self.swipe_up, locator=about_menu_btn, max_swipes=5)
        self.click(about_menu_btn)
        return SettingsAboutPage(driver=self.driver)
