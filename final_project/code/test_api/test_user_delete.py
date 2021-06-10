import pytest

from test_api.base import ApiBaseCase
from faker import Faker

fake = Faker()


class TestApiUserDelete(ApiBaseCase):
    """
    **Tests:**
        * Correct user delete
        * Invalid user name
        * Invalid methods
    """

    def prepare(self):
        admin = self.mysql_builder.create_user()
        self.app_api_client.login(admin.username, admin.password)

    def test_delete(self):
        user = self.mysql_builder.create_user()

        self.app_api_client.delete_user(username=user.username)

        query = self.mysql_builder.select_user(username=user.username)
        assert query is None

    @pytest.mark.parametrize('username',
                             [fake.lexify('????????'), ''],
                             ids=['Random username', 'Empty username'])
    def test_invalid_username(self, username):
        expected_status = 404
        resp = self.app_api_client.delete_user(username=username, expected_status=[expected_status])

        assert resp.status_code == expected_status

    @pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE', 'PATCH'])
    @pytest.mark.BUG
    def test_invalid_methods(self, method):
        user = self.mysql_builder.create_user()

        self.app_api_client.delete_user(username=user.username, expected_status=[405])

        query = self.mysql_builder.select_user(username=user.username)
        assert query is None
