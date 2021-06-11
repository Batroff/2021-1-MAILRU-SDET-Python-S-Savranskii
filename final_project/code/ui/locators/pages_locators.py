from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class AuthPageLocators(BasePageLocators):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BTN = (By.ID, 'submit')

    LOGIN_ERROR = (By.ID, 'flash')

    REGISTER_PAGE = (By.CSS_SELECTOR, 'a[href="/reg"]')


class RegisterPageLocators(AuthPageLocators):
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_CONFIRM_INPUT = (By.ID, 'confirm')
    CHECKBOX_INPUT = (By.ID, 'term')

    REGISTER_ERROR = AuthPageLocators.LOGIN_ERROR


class MenuLocators(BasePageLocators):
    MENU_LINK_TEMPLATE = (By.XPATH, '//a[text()="{0}"]')
    MENU_USERNAME = (By.XPATH, '//div[@id="login-name"]//li[contains(text(), "Logged as")]')
    MENU_VK_ID = (By.XPATH, '//div[@id="login-name"]//li[contains(text(), "VK ID:")]')
    MENU_LOGOUT = (By.XPATH, '//a[text()="Logout"]')


class HomePageLocators(MenuLocators):
    IMAGE_LINK_BY_TITLE_TEMPLATE = (By.XPATH, '//div[div[text()="{0}"]]')
