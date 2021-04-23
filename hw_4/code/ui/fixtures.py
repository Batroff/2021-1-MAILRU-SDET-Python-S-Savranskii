import os

import allure
import pytest
from appium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


def get_driver(appium_url, repo_root):
    capability = {
        "platformName": "Android",
        "platformVersion": "8.1",
        "automationName": "Appium",
        "appPackage": "ru.mail.search.electroscope",
        "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
        "app": os.path.join(repo_root, 'stuff', 'Marussia_v1.39.1.apk'),
        "orientation": "PORTRAIT",
        "autoGrantPermissions": True
    }
    driver = webdriver.Remote(appium_url, desired_capabilities=capability)
    return driver


@pytest.fixture(scope='function')
def driver(config, repo_root):
    appium_url = config['appium']
    browser = get_driver(appium_url, repo_root)
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)