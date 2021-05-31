from ui.locators.pages_locators import HomePageLocators
from ui.pages.base_page import BasePage


class HomePage(BasePage):

    url = 'http://localhost:8080/welcome/'
    locators = HomePageLocators()
