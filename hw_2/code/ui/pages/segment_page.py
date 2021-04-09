import logging
import time

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from ui.locators.pages_locators import SegmentPageLocators
from ui.pages.base_page import BasePage, ElementNotExistsException
from utils.decorators import wait

logger = logging.getLogger('test')


class SearchQueryNotFoundException(Exception):
    pass


class SegmentPage(BasePage):

    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentPageLocators()

    def go_to_segment_list(self):
        self.click(self.locators.SEGMENT_LIST_BTN)

    @allure.step('Create segment')
    def create_segment(self, name, source_id, timeout=10):
        locators = [self.locators.CREATE_FIRST_SEGMENT, self.locators.CREATE_SEGMENT]

        element_locator = wait(method=self.check_one_of_clickable, locators=locators,
                               timeout=timeout, interval=0.2, check=True, error=ElementNotExistsException)
        self.click(element_locator)

        # Select source of segment (context targeting)
        self.click(self.locators.SELECT_GROUPS_TARGETING)
        self.click(self.format_locator(self.locators.GROUP_CHECKBOX, source_id))
        self.click(self.locators.SEGMENT_ADD_BTN)

        # Change segment name
        self.keys_to_input(locator=self.locators.SEGMENT_INPUT_NAME, keys=name)

        self.click(self.locators.CREATE_SEGMENT)

    @allure.step('Create source of data (context targeting)')
    def create_group_source(self, link):
        self.click(self.locators.GO_TO_GROUPS_VK_OK)
        self.keys_to_input(locator=self.locators.GROUP_LINK_INPUT, keys=link)
        self.click(self.locators.GROUPS_SELECT_ALL)
        self.click(self.locators.GROUPS_ADD_SELECTED)
        group_row = self.find(self.format_locator(self.locators.GROUP_ROW_TEMPLATE, "Подслушано РТУ МИРЭА (МТУ)"))
        return group_row.find_element(*self.locators.GROUP_ROW_ID).text

    @allure.step('Remove segment and check existence of it')
    def remove_segment(self, name):
        locator = self.format_locator(self.locators.SEGMENT_NAME_TEMPLATE, name)
        segment_id = self.find(locator).get_attribute('href').split('/')[-1]

        locator = self.format_locator(self.locators.SEGMENT_CHECKBOX_TEMPLATE, segment_id)
        self.click(locator)

        self.click(self.locators.SEGMENT_ACTIONS)
        self.click(self.locators.SEGMENT_ACTION_REMOVE)

        def _check():
            if self.element_exists(self.locators.SEGMENT_REMOVE_SUCCESS):
                return True

        wait(_check, timeout=10, interval=0.2)

    @allure.step('Check segment if segment exists')
    def segment_exists(self, name):
        search = self.find(self.locators.SEGMENTS_SEARCH)
        search.clear()
        search.send_keys(name)
        search.send_keys(Keys.ENTER)

        def _check_search(query):
            if self.element_exists(self.locators.SEARCH_NOT_FOUND):
                return "Not exists"
            elif self.element_exists(self.locators.SEARCH_FOUND):
                return "Exists"

            raise SearchQueryNotFoundException(f'{query} error in {self.__class__.__name__}')

        return wait(_check_search, timeout=10, interval=0.2, error=SearchQueryNotFoundException, query=name)
