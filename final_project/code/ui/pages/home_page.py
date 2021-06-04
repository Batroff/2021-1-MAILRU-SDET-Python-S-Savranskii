from ui.locators.pages_locators import HomePageLocators
from ui.pages.base_page import BasePage


class HomePage(BasePage):

    url = 'http://test_app:8081/welcome/'
    locators = HomePageLocators()
