import os

import allure
import pytest
from _pytest.config import Config

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
    url = f'http://test_app:{config["APP_PORT"]}'

    browser = get_driver(config=config, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()

    yield browser

    browser.quit()


def get_driver(config, download_dir):
    options = ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir})

    if config['selenoid']:
        caps = {
            'browserName': 'chrome',
            'browserVersion': '91.0_vnc',
            "selenoid:option": {
                "enableVNC": True,
            },
            "additionalNetworks": ["testing_network"]
        }
        browser = webdriver.Remote(command_executor=config['selenoid'],
                                   options=options,
                                   desired_capabilities=caps)
    else:
        manager = ChromeDriverManager(version='latest')
        browser = webdriver.Chrome(executable_path=manager.install(),
                                   options=options)

    return browser


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
