import allure
import pytest
from faker import Faker

from mysql.models import User
from test_api.base import ApiBaseCase

fake = Faker()


class TestApiUserAccept(ApiBaseCase):
    """
    **Tests:**
        * Correct user accept (with access = 0)
        * User accept (with access = 1)
        * Invalid user name
        * Invalid methods
    """

    def prepare(self):
        admin = self.mysql_builder.create_user()
        self.app_api_client.login(admin.username, admin.password)

    @allure.description("Positive accept user case, expect access = 1, expected_status 304")
    def test_accept_user(self):
        user = self.mysql_builder.create_user(access=0)

        self.app_api_client.accept_user(username=user.username)

        query = self.mysql_builder.select_user(username=user.username)
        assert isinstance(query, User)
        assert query.access == 1

    @allure.description("Accept user with access = 1, expect access = 1, expected_status 304")
    def test_accept_user_with_access(self):
        user = self.mysql_builder.create_user()

        self.app_api_client.accept_user(username=user.username, expected_status=[304])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 1

    @pytest.mark.parametrize('username',
                             [fake.lexify('????????'), ''],
                             ids=['Random username', 'Empty username'])
    @allure.description("Accept not-existent user, expect 404 status code from API")
    def test_invalid_username(self, username):
        expected_status = 404
        resp = self.app_api_client.accept_user(username=username, expected_status=[expected_status])

        assert resp.status_code == expected_status

    @pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE', 'PATCH'])
    @pytest.mark.BUG
    @allure.description("Accept user by invalid methods, expect 405 status code from API")
    def test_invalid_methods(self, method):
        user = self.mysql_builder.create_user(access=0)

        self.app_api_client.accept_user(username=user.username, expected_status=[405])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 0
