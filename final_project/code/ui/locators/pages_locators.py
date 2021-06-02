from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class AuthPageLocators(BasePageLocators):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    SUBMIT_BTN = (By.ID, 'submit')

    LOGIN_ERROR_TEMPLATE = (By.XPATH, '//div[@id="flash" and text()="{0}"]')

    REGISTER_PAGE = (By.CSS_SELECTOR, 'a[href="/reg"]')


class HomePageLocators(BasePageLocators):
    pass


class RegisterPageLocators(AuthPageLocators):
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_CONFIRM_INPUT = (By.ID, 'confirm')
    CHECKBOX_INPUT = (By.ID, 'term')

    REGISTER_ERROR_TEMPLATE = AuthPageLocators.LOGIN_ERROR_TEMPLATE
