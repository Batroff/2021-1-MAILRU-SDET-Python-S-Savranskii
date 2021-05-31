from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class AuthPageLocators(BasePageLocators):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BTN = (By.ID, 'submit')
    # LOGIN_ERROR = (By.ID, 'flash')
    LOGIN_ERROR_TEMPLATE = (By.XPATH, '//div[@id="flash" and text()="{0}"]')


class HomePageLocators(BasePageLocators):
    pass