from appium.webdriver.common.mobileby import MobileBy


class BasePageLocators:
    package = 'ru.mail.search.electroscope'


class MainPageLocators(BasePageLocators):
    package = BasePageLocators.package

    OPEN_CHAT = (MobileBy.ID, f'{package}:id/keyboard')
    OPEN_SETTINGS = (MobileBy.ID, f'{package}:id/assistant_menu_bottom')


class ChatPageLocators(BasePageLocators):
    package = BasePageLocators.package

    CHAT_INPUT = (MobileBy.ID, f'{package}:id/input_text')
    CHAT_INPUT_SEND = (MobileBy.ID, f'{package}:id/text_input_send')
    CARD_TITLE_TEMPLATE = (MobileBy.XPATH, '//*[contains(@resource-id, "item_dialog_fact_card_title") and @text="{0}"]')

    SUGGESTS_LIST = (MobileBy.ID, f'{package}:id/suggests_list')
    SUGGESTS_ITEM_TEMPLATE = (MobileBy.XPATH, '//*[contains(@resource-id, "item_suggest_text") and @text="{0}"]')

    DIALOG_ITEM_TEMPLATE = (MobileBy.XPATH, '//*[contains(@resource-id, "dialog_item") and @text="{0}"]')

    PLAYER_NAME_TEMPLATE = (MobileBy.XPATH, '//*[contains(@resource-id, "player_track_name") and @text="{0}"]')


class SettingsPageLocators(BasePageLocators):
    package = BasePageLocators.package

    FEED_SOURCE_MENU = (MobileBy.ID, f'{package}:id/user_settings_field_news_sources')
    ABOUT_MENU = (MobileBy.ID, f'{package}:id/user_settings_about')


class SettingsAboutPageLocators(BasePageLocators):
    package = BasePageLocators.package

    ABOUT_PROGRAM_VERSION = (MobileBy.ID, f'{package}:id/about_version')
    ABOUT_PROGRAM_TRADEMARK = (MobileBy.ID, f'{package}:id/about_copyright')


class SettingsSourcePageLocators(BasePageLocators):
    package = BasePageLocators.package

    FEED_SOURCE_ITEM_TITLE_TEMPLATE = (
        MobileBy.XPATH,
        '//*[contains(@resource-id, "item_title") and @text="{0}"]'
    )
    FEED_SOURCE_ITEM_SELECTED_TEMPLATE = (
        MobileBy.XPATH,
        '//*[@text="{0}"]//following-sibling::*[contains(@resource-id, "selected")]'
    )

