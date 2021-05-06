import logging
import time

import allure

from ui.locators.locators_android import ChatPageLocators
from ui.pages.base_page import BasePage


class NotFoundCardException(Exception):
    pass


logger = logging.getLogger('test')


class ChatPage(BasePage):
    locators = ChatPageLocators()

    @allure.step('Find {text} in chat')
    def find_in_chat(self, text):
        chat_input = self.find(self.locators.CHAT_INPUT)
        chat_input.clear()
        chat_input.send_keys(text)
        self.driver.hide_keyboard()
        self.click(self.locators.CHAT_INPUT_SEND)

    def get_news(self):
        self.find_in_chat('News')
        return self.get_player_vesti_fm()

    def get_player_vesti_fm(self):
        return self._get_player_name('Вести ФМ')

    @allure.step('Get news player {name} title')
    def _get_player_name(self, name):
        return self.find(self.format_locator(self.locators.PLAYER_NAME_TEMPLATE, name)).text

    def get_dialog_calc_result(self):
        return self._get_dialog_item_text('6')

    @allure.step('Get text in dialog item with "{text}"')
    def _get_dialog_item_text(self, text):
        return self.find(self.format_locator(self.locators.DIALOG_ITEM_TEMPLATE, text)).text

    def get_card_title_russia(self):
        return self._get_card_title('Россия')

    def get_card_title_population(self):
        return self._get_card_title('146 млн.')

    @allure.step('Get result card with {text} title')
    def _get_card_title(self, text):
        return self.find(self.format_locator(self.locators.CARD_TITLE_TEMPLATE, text)).text

    def click_on_population_suggest(self):
        self._find_element_in_suggests(
            self.format_locator(self.locators.SUGGESTS_ITEM_TEMPLATE,
                                'численность населения россии')
        )

    @allure.step('Swipe to {locator} in suggests')
    def _find_element_in_suggests(self, locator):
        self.swipe_to_element(swipe_method=self.swipe_element_lo_left, locator=locator,
                              max_swipes=5, container_locator=self.locators.SUGGESTS_LIST)
        self.click(locator)
