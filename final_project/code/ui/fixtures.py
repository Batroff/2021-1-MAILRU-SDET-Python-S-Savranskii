import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.auth_page import AuthPage
from ui.pages.base_page import BasePage


@pytest.fixture
def base_page(driver) -> BasePage:
    return BasePage(driver=driver)


@pytest.fixture
def auth_page(driver) -> AuthPage:
    return AuthPage(driver=driver)


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']

    browser = get_driver(download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()

    yield browser

    browser.quit()


def get_driver(download_dir):
    options = ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir})
    manager = ChromeDriverManager(version='latest')
    browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    return browser
