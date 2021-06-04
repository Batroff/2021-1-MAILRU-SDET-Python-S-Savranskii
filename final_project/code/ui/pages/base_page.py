import logging

import allure
from selenium.common.exceptions import StaleElementReferenceException
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

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
        assert self.is_opened(self._url_equals)

    def is_opened(self, check_method=None):
        if check_method is None:
            check_method = self._url_equals
        return wait(check_method, error=PageNotLoadedException, check=True, timeout=self.DEFAULT_TIMEOUT, interval=0.2)

    def _url_equals(self):
        if self.driver.current_url != self.url:
            raise PageNotLoadedException(
                f'{self.url} did not opened in {self.DEFAULT_TIMEOUT} for {self.__class__.__name__}.\n'
                f'Current url: {self.driver.current_url}.')
        return True

    def _url_contains(self):
        if self.url not in self.driver.current_url:
            raise PageNotLoadedException(
                f'{self.url} did not opened in {self.DEFAULT_TIMEOUT} for {self.__class__.__name__}.\n'
                f'Current url: {self.driver.current_url}.')
        return True

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        return WebDriverWait(self.driver, timeout)

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
        self.driver.refresh()

    @allure.step('Upload file')
    def upload_file(self, locator, file):
        self.find(locator).send_keys(file)

    # def check_one_of_clickable(self, locators):
    #     for locator in locators:
    #         if self.element_exists(locator):
    #             if self.find(locator).is_displayed():
    #                 return locator
    #
    #     raise ElementNotExistsException(
    #         f'Create button hadn\'t been found for {self.__class__.__name__}.'
    #     )
