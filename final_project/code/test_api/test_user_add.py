import allure

from test_api.base import ApiBaseCase
from data_fixtures import *


class TestApiUserAdd(ApiBaseCase):
    """
    **Tests:**
        * Correct user
        * Duplicate user
        * Invalid username
        * Invalid password
        * Invalid email
        * Invalid headers
        * Invalid method
    """

    def prepare(self):
        admin = self.mysql_builder.create_user()
        self.app_api_client.login(admin.username, admin.password)

    @pytest.mark.BUG
    @allure.description("Positive add user case, expect user in db")
    def test_add_user(self, test_user):
        self.app_api_client.add_user(username=test_user.username,
                                     password=test_user.password,
                                     email=test_user.email)

        query = self.mysql_builder.select_user(username=test_user.username)
        assert isinstance(query, User)

    @pytest.mark.parametrize("invalid_user,expected_status", [
        ({"username": fake.lexify('?' * 5)}, [400]),
        ({"username": fake.lexify('?' * 20)}, [400]),
        ({"email": f"{fake.lexify('?')}@{fake.lexify('?')}.{fake.lexify('?')}"}, [400]),
        ({"email": fake.lexify('?' * 64) + '@test.ru'}, [400]),
        ({"password": fake.password(length=256)}, [400])
    ], ids=[
        "username_short",
        "username_long",
        "email_short",
        "email_long",
        "password_long"
    ])
    @pytest.mark.BUG
    @allure.description("Add user with invalid data, expect 400 status code from API, user is not in db")
    def test_invalid_data(self, invalid_user, expected_status):
        user = self.mysql_builder.create_user(push=False)
        username = invalid_user.get("username", user.username)
        email = invalid_user.get("email", user.email)
        password = invalid_user.get("password", user.password)

        self.app_api_client.add_user(username=username,
                                     email=email,
                                     password=password,
                                     expected_status=expected_status)  # 210

        query = self.mysql_builder.select_user(username=user.username)
        assert query is None

    @allure.description("Add user with duplicate username, expect 304 status code from API, only one user in db")
    def test_duplicate_username(self, test_user):
        user = self.mysql_builder.create_user()

        self.app_api_client.add_user(username=user.username, password=test_user.password,
                                     email=test_user.email, expected_status=[304])

        query = self.mysql_builder.select_user(username=user.username)
        assert isinstance(query, User)

    @pytest.mark.BUG
    @allure.description("Add user with duplicate email, expect 304 status code from API, only one user in db")
    def test_duplicate_email(self, test_user):
        user = self.mysql_builder.create_user()

        self.app_api_client.add_user(username=test_user.username, password=test_user.password,
                                     email=user.email, expected_status=[304])

        query = self.mysql_builder.select_user(email=user.email)
        assert isinstance(query, User)

    @pytest.mark.BUG
    @allure.description("Add user with invalid methods, expect 400 status code from API, user is not in db")
    def test_invalid_headers(self, test_user):
        self.app_api_client.add_user(username=test_user.username,
                                     password=test_user.password,
                                     email=test_user.email,
                                     headers={},
                                     expected_status=[400])

        query = self.mysql_builder.select_user(username=test_user.username)
        assert query is None

    @pytest.mark.parametrize("method", ['GET', 'PUT', 'DELETE', 'HEAD', pytest.param('OPTIONS', marks=pytest.mark.BUG),
                                        'CONNECT', 'TRACE', 'PATCH'])
    @allure.description("Add user by invalid methods, expect 405 status code from API")
    def test_invalid_method(self, test_user, method):
        self.app_api_client.add_user(username=test_user.username,
                                     password=test_user.password,
                                     email=test_user.email,
                                     method=method,
                                     expected_status=[405])

        query = self.mysql_builder.select_user(username=test_user.username)
        assert query is None
