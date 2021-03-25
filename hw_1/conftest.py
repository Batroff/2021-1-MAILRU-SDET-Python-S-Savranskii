from selenium import webdriver
import pytest


def pytest_addoption(parser):
    parser.addoption("--url", default="http://target.my.com")


@pytest.fixture(scope="session")
def config(request):
    url = request.config.getoption("--url")
    return {"url": url}


@pytest.fixture(scope="function")
def driver(config):
    url = config["url"]

    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()

    yield browser
    browser.close()
