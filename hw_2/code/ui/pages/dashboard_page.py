import logging
import time

import allure

from ui.locators.pages_locators import DashboardPageLocators
from ui.pages.base_page import BasePage, ElementNotExistsException
from ui.pages.campaign_page import CampaignPage
from ui.pages.segment_page import SegmentPage

from utils.decorators import wait


class CampaignException(Exception):
    pass


logger = logging.getLogger('test')


class DashboardPage(BasePage):
    locators = DashboardPageLocators()
    url = 'https://target.my.com/dashboard'

    def go_to_segments(self):
        locator = self.format_locator(self.locators.HEAD_MENU_LINK_TEMPLATE, 'Аудитории')
        self.click(locator)
        return SegmentPage(driver=self.driver)

    @allure.step('Create campaign')
    def create_campaign(self, timeout=10):

        locators = [self.locators.CREATE_FIRST_CAMPAIGN, self.locators.CREATE_CAMPAIGN]
        element_locator = wait(self.check_one_of_clickable, timeout=timeout, interval=0.2, check=True,
                               error=ElementNotExistsException, locators=locators)
        self.click(element_locator)

        return CampaignPage(driver=self.driver)

    @allure.step('Check exist of created campaign')
    def campaign_exists(self, name):
        def _check(n):
            locator = self.format_locator(self.locators.CAMPAIGN_NAME_TEMPLATE, n)
            if self.element_exists(locator):
                return True

            raise CampaignException(f'Campaign hadn\'t been found for {self.__class__.__name__}.')

        return wait(_check, timeout=10, interval=0.2, n=name)

    @allure.step('Select campaign')
    def select_campaign(self, name):
        self.click(self.format_locator(self.locators.CAMPAIGN_CHECKBOX, name))

    @allure.step('Remove created campaign')
    def remove_campaign(self):
        self.click(self.locators.CAMPAIGN_ACTIONS)
        self.click(self.locators.CAMPAIGN_REMOVE)
