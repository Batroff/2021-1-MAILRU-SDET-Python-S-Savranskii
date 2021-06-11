import random

import allure
import pytest
from faker import Faker

from test_ui.base import BaseCase

fake = Faker()


class TestAuthPage(BaseCase):
    """
    **Тесты:**
     * негативный на длину логина
     * на корректный логин с доступом 1
     * на корректный логин с доступом 0
     * на неправильный логин
    """

    @pytest.mark.parametrize('user_data', [
        {
            'username': fake.lexify('?' * i),
            'password': fake.password()
        } for i in [random.randint(1, 5), random.randint(17, 200)]
    ])
    @pytest.mark.UI
    @allure.description("Login validation check")
    def test_login_len_negative(self, user_data):
        self.auth_page.login(username=user_data['username'], password=user_data['password'], get_home_page=False)

        assert self.auth_page.is_error_exists('Incorrect username length')

    @pytest.mark.UI
    @allure.description("Positive login case; user.active must switch to 1, page redirect to home_page")
    def test_correct_login(self):
        user_with_access = self.mysql_builder.create_user()
        username, password = user_with_access.username, user_with_access.password

        home_page = self.auth_page.login(username=username, password=password)

        user = self.mysql_builder.select_user(username=username)
        assert user.active == 1

        assert home_page.is_opened()

    @pytest.mark.UI
    @allure.description("Login by banned user data, user.active must stay at 0, without redirect, expecting error")
    def test_login_without_access(self):
        user_without_access = self.mysql_builder.create_user(access=0)
        username, password = user_without_access.username, user_without_access.password

        self.auth_page.login(username=username, password=password, get_home_page=False)

        user = self.mysql_builder.select_user(username=username)
        assert user.active == 0

        assert self.auth_page.is_error_exists('Ваша учетная запись заблокирована')

    @pytest.mark.UI
    @allure.description("Login by non-existing user data, expecting error")
    def test_wrong_data_login(self):
        username = fake.lexify('??????')
        password = fake.bothify('#?#?#?#?')

        self.auth_page.login(username=username, password=password, get_home_page=False)

        assert self.auth_page.is_error_exists('Invalid username or password')
