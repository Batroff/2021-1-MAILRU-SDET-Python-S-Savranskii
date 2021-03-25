from selenium.webdriver.common.by import By

# Main page
MAIN_PAGE_LOGIN_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")

# Login popup
INPUT_EMAIL_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm') and @name='email']")
INPUT_PASSWORD_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm') and @name='password']")
FORM_LOGIN_BTN_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm') and text()='Войти']")

# Logged in pages
OPEN_MENU_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightWrap-') and //a[@href='/logout']]")
LOGOUT_BTN_LOCATOR = (By.XPATH, "//a[@href='/logout']")

CONTACT_PAGE_BTN_LOCATOR = (By.XPATH, "//a[@href='/profile']")
CONTACT_INPUT_FIO_LOCATOR = (By.XPATH, "//div[contains(@data-name, 'fio')]//input")
CONTACT_INPUT_PHONE_LOCATOR = (By.XPATH, "//div[contains(@data-name, 'phone')]//input")
CONTACT_INPUT_EMAIL_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-additional-email')]//input")
CONTACT_SUBMIT_LOCATOR = (By.XPATH, "//button[@data-class-name='Submit']")
CONTACT_SUCCESS_INDICATOR = (By.XPATH, "//div[text()='Информация успешно сохранена']")

BILLING_PAGE_BTN_LOCATOR = (By.XPATH, "//a[@href='/billing']")
BILLING_DEPOSIT_BTN_LOCATOR = (By.XPATH, "//input[@type='button' and @value='Пополнить счёт']")

STATISTICS_PAGE_BTN_LOCATOR = (By.XPATH, "//a[@href='/statistics']")
