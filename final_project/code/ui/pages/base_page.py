import logging
import os

import allure
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from ui.locators.pages_locators import BasePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.decorators import wait


class PageNotLoadedException(Exception):
    pass


class TextNotChangedException(Exception):
    pass


class ElementNotExistsException(Exception):
    pass


logger = logging.getLogger('pytest')


class BasePage(object):
    DEFAULT_TIMEOUT = 15
    CLICK_RETRY = 3

    locators = BasePageLocators()
    url = None
    host = 'test_app'
    port = os.environ.get('APP_PORT', '8081')

    def __init__(self, driver):
        self.driver: webdriver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
        assert self.is_opened(self._url_equals)

    def is_opened(self, check_method=None):
        if check_method is None:
            check_method = self._url_equals
        return wait(check_method, error=PageNotLoadedException, check=True, timeout=self.DEFAULT_TIMEOUT, interval=0.2)

    def _url_equals(self):
        if self.driver.current_url not in self.url:
            raise PageNotLoadedException(
                f'{self.url} did not opened in {self.DEFAULT_TIMEOUT} for {self.__class__.__name__}.\n'
                f'Current url: "{self.driver.current_url}".')
        return True

    def find(self, locator, timeout=None) -> WebElement:
        logger.info(f'Finding element "{locator}"...')
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        return WebDriverWait(self.driver, timeout)

    @allure.step('Click on {locator}')
    def click(self, locator, timeout=None):
        for i in range(self.CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {self.CLICK_RETRY}...')
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == self.CLICK_RETRY - 1:
                    raise

    def keys_to_input(self, locator, keys):
        logger.info(f'Sending keys "{keys}" to {locator}')
        inp = self.wait().until(EC.element_to_be_clickable(locator))
        inp.clear()
        inp.send_keys(keys)

    def element_exists(self, locator) -> bool:
        return len(self.driver.find_elements(*locator)) != 0

    @staticmethod
    def format_locator(locator, *args) -> tuple:
        return locator[0], locator[1].format(*args)

    @allure.step('Refresh page')
    def refresh_page(self):
        logger.info(f'Refreshing page "{self.driver.current_url}"')
        self.driver.refresh()

    @allure.step('Upload file')
    def upload_file(self, locator, file):
        logger.info(f'Uploading file "{file}" to "{locator}"')
        self.find(locator).send_keys(file)

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait_text_in_element(self, locator, text, timeout=None):
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        return self.wait(timeout=timeout) \
            .until(EC.text_to_be_present_in_element(locator=locator, text_=text))
