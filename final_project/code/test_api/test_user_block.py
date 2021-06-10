import allure
import pytest
from faker import Faker

from test_api.base import ApiBaseCase

fake = Faker()


class TestApiUserBlock(ApiBaseCase):
    """
    **Tests:**
        * Correct user block (with access = 1)
        * User block (with access = 0)
        * Invalid user name
        * Invalid methods
    """

    def prepare(self):
        admin = self.mysql_builder.create_user()
        self.app_api_client.login(admin.username, admin.password)

    @allure.description("Positive block user case, expect access change to 0")
    def test_block(self):
        user = self.mysql_builder.create_user()

        self.app_api_client.block_user(username=user.username)

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 0

    @allure.description("Block banned user, expect access doesn't change")
    def test_block_banned_user(self):
        user = self.mysql_builder.create_user(access=0)

        self.app_api_client.block_user(username=user.username, expected_status=[304])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 0

    @pytest.mark.parametrize('username',
                             [fake.lexify('????????'), ''],
                             ids=['Random username', 'Empty username'])
    def test_invalid_username(self, username):
        expected_status = 404
        resp = self.app_api_client.block_user(username=username, expected_status=[expected_status])

        assert resp.status_code == expected_status

    @pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE', 'PATCH'])
    @pytest.mark.BUG
    @allure.description("Block user by invalid methods, expect 405 status code from API")
    def test_invalid_methods(self, method):
        user = self.mysql_builder.create_user()

        self.app_api_client.block_user(username=user.username, expected_status=[405])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 1
