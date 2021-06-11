import os

import allure
import pytest

from test_ui.base import BaseCase


class TestHomePageMenu(BaseCase):
    """
    **Navigation**
        * HOME - '/'
        * Python - 'https://www.python.org/'\n
          * Python history - 'https://en.wikipedia.org/wiki/History_of_Python'
          * About flask - 'https://flask.palletsprojects.com/en/1.1.x/#'
        * Linux:\n
          * Centos - 'https://getfedora.org/ru/workstation/download/'
        * Network:\n
          * Wireshark news - 'https://www.wireshark.org/news/'
          * Wireshark download - 'https://www.wireshark.org/#download'
          * Tcpdump examples - 'https://hackertarget.com/tcpdump-examples/'

    **Controls panel**
        * Logged as ``<name>``
        * VK ID: ``<ID>``
        * Logout button
    """

    authorize = True

    @pytest.mark.UI
    @allure.description("When user logs out, flag user.active should change from 1 to 0 and url redirected to auth_page")
    def test_logout_button(self):
        self.home_page.logout()

        username = os.environ.get('USER_USERNAME')
        user = self.mysql_builder.select_user(username=username)

        assert user.active == 0
        assert self.auth_page.is_opened()

    @pytest.mark.UI
    @allure.description("Username must match displayed name in menu")
    def test_logged_name(self):
        menu_username = self.home_page.get_username()
        curr_username = os.environ.get('USER_USERNAME')

        assert curr_username == menu_username

    @pytest.mark.UI
    @allure.description("Vk_id must match displayed name in menu")
    def test_vk_id(self):
        menu_id = self.home_page.get_vk_id()

        username = os.environ.get('USER_USERNAME')
        curr_id = self.vk_api_client.get_vk_id(username=username)

        assert menu_id == curr_id

    @pytest.mark.UI
    @allure.description("Redirect to home page from menu")
    def test_home_link(self):
        self.home_page = self.home_page.go_to_home_page()
        assert self.home_page.is_opened()

    @pytest.mark.UI
    @allure.description("Redirect to python page from menu")
    def test_python_link(self):
        self.home_page.go_to_linked_page('Python')
        assert 'https://www.python.org/' == self.driver.current_url

    @allure.description("Redirect to external pages (some open in new window) from dropdown navigation menu")
    @pytest.mark.parametrize("link_params,expected_url", [
        ({'header': 'Python', 'dropdown': 'Python history'}, 'https://en.wikipedia.org/wiki/History_of_Python'),
        ({'header': 'Python', 'dropdown': 'About Flask'}, 'https://flask.palletsprojects.com/en/1.1.x/#'),
        ({'header': 'Linux', 'dropdown': 'Download Centos7'}, 'https://getfedora.org/ru/workstation/download/'),
        ({'header': 'Network', 'dropdown': 'News'}, 'https://www.wireshark.org/news/'),
        ({'header': 'Network', 'dropdown': 'Download'}, 'https://www.wireshark.org/#download'),
        ({'header': 'Network', 'dropdown': 'Examples '}, 'https://hackertarget.com/tcpdump-examples/'),
    ], ids=[
        'Python history',
        'About Flask',
        'Download Centos7',
        'Network News',
        'Network Download',
        'Network Examples',
    ])
    @pytest.mark.UI
    def test_dropdown_link(self, link_params, expected_url):
        target = self.home_page.get_link_target(link_text=link_params['dropdown'])

        self.home_page.go_to_dropdown_linked_page(header_name=link_params['header'],
                                                  dropdown_name=link_params['dropdown'])

        if target == '_blank':
            handler = self.driver.current_window_handle
            self.home_page.switch_to_next_tab(current_window_handler=handler)

        assert self.driver.current_url == expected_url


class TestHomePageBody(BaseCase):
    """
    **Image links:**
        * What is an API?
        * Future of internet
        * Lets talk about SMTP?
    """

    authorize = True

    @pytest.mark.parametrize("link_name,expected_url", [
        pytest.param('What is an API?',
                     'https://en.wikipedia.org/wiki/API',
                     marks=pytest.mark.UNSTABLE),
        ('Future of internet',
         'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'),
        ('Lets talk about SMTP?',
         'https://ru.wikipedia.org/wiki/SMTP'),
    ], ids=[
        'What is an API?',
        'Future of internet',
        'Lets talk about SMTP?',
    ])
    @pytest.mark.UI
    @allure.description("Redirect to external pages from image")
    def test_image_links(self, link_name, expected_url):
        self.home_page.go_to_image_linked_page(link_name)

        handler = self.driver.current_window_handle
        self.home_page.switch_to_next_tab(current_window_handler=handler)

        assert self.driver.current_url == expected_url
