import pytest
from time import sleep
from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 5
CLICK_RETRY = 3


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT

        return WebDriverWait(self.driver, timeout)

    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def go_to_contacts(self):
        self.click(basic_locators.CONTACT_PAGE_BTN_LOCATOR)

    def contacts_change_name(self, name=None, timeout=None):
        self.input_send_keys(basic_locators.CONTACT_INPUT_FIO_LOCATOR, timeout=timeout, keys=name)

    def contacts_change_phone(self, phone=None, timeout=None):
        self.input_send_keys(basic_locators.CONTACT_INPUT_PHONE_LOCATOR, timeout=timeout, keys=phone)

    def contacts_change_email(self, email=None, timeout=None):
        self.input_send_keys(basic_locators.CONTACT_INPUT_EMAIL_LOCATOR, timeout=timeout, keys=email)

    def contacts_save_changes(self, timeout=None):
        self.click(basic_locators.CONTACT_SUBMIT_LOCATOR, timeout=timeout)
        self.wait(5).until(EC.visibility_of_element_located(basic_locators.CONTACT_SUCCESS_INDICATOR))

    def contacts_get_info(self, timeout=None):
        name = self.find(basic_locators.CONTACT_INPUT_FIO_LOCATOR, timeout).get_attribute('value')
        phone = self.find(basic_locators.CONTACT_INPUT_PHONE_LOCATOR, timeout).get_attribute('value')
        email = self.find(basic_locators.CONTACT_INPUT_EMAIL_LOCATOR, timeout).get_attribute('value')
        return {"name": name, "phone": phone, "email": email}

    def logout(self):
        self.click(basic_locators.OPEN_MENU_LOCATOR)
        sleep(1)

        self.find(basic_locators.LOGOUT_BTN_LOCATOR).click()
        self.wait(5).until(EC.title_contains("myTarget"))

    def login(self, login, password):
        # Login button
        self.click(basic_locators.MAIN_PAGE_LOGIN_BTN_LOCATOR)

        # Form
        self.input_send_keys(basic_locators.INPUT_EMAIL_LOCATOR, timeout=None, keys=login)
        self.input_send_keys(basic_locators.INPUT_PASSWORD_LOCATOR, timeout=None, keys=password)
        self.click(basic_locators.FORM_LOGIN_BTN_LOCATOR)

        # Wait login
        self.wait(5).until(EC.title_is("Кампании"))

    def input_send_keys(self, locator, timeout=None, keys=None):
        if keys is None:
            keys = ""

        input_elem = self.find(locator, timeout)
        input_elem.clear()
        input_elem.send_keys(keys)

    def switch_page(self, page, timeout=None):
        page_locators = {
            "Профиль": basic_locators.CONTACT_PAGE_BTN_LOCATOR,
            "Баланс": basic_locators.BILLING_PAGE_BTN_LOCATOR,
            "Статистика": basic_locators.STATISTICS_PAGE_BTN_LOCATOR,
        }

        current_url = self.driver.current_url
        self.click(page_locators[page], timeout)
        self.wait(timeout).until(EC.url_changes(current_url))
