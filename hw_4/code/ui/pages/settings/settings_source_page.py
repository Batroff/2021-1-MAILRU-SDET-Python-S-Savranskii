from ui.locators.locators_android import SettingsSourcePageLocators
from ui.pages.base_page import BasePage


class FeedSourceNotSetException(Exception):
    pass


class SettingsSourcePage(BasePage):
    locators = SettingsSourcePageLocators()

    def set_source(self, name):
        self.click(self.format_locator(self.locators.FEED_SOURCE_ITEM_TITLE_TEMPLATE, name))

    def is_feed_source_set(self, name):
        if self.find(self.format_locator(self.locators.FEED_SOURCE_ITEM_SELECTED_TEMPLATE, name)):
            return True
        raise FeedSourceNotSetException(f'Feed source "{name} is not set"')
