import allure

from test_api.base import ApiBaseCase

from data_fixtures import *


class TestUnauthorizedApiOperations(ApiBaseCase):
    """
    **Tests:**
        * Unauthorized add user
        * Unauthorized delete user
        * Unauthorized block user
        * Unauthorized block user
    """

    @allure.description("Api request without authorization, expect 401")
    def test_unauthorized_user_add(self, test_user):
        self.app_api_client.add_user(username=test_user.username,
                                     password=test_user.password,
                                     email=test_user.email,
                                     expected_status=[401])

        query = self.mysql_builder.select_user(username=test_user.username)
        assert query is None

    @allure.description("Api request without authorization, expect 401")
    def test_unauthorized_user_delete(self):
        user = self.mysql_builder.create_user()

        self.app_api_client.delete_user(username=user.username,
                                        expected_status=[401])

        query = self.mysql_builder.select_user(username=user.username)
        assert isinstance(query, User)

    @allure.description("Api request without authorization, expect 401")
    def test_unauthorized_user_block(self):
        user = self.mysql_builder.create_user()

        self.app_api_client.block_user(username=user.username,
                                       expected_status=[401])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 1

    @allure.description("Api request without authorization, expect 401")
    def test_unauthorized_user_accept(self):
        user = self.mysql_builder.create_user(access=0)

        self.app_api_client.accept_user(username=user.username,
                                        expected_status=[401])

        query = self.mysql_builder.select_user(username=user.username)
        assert query.access == 0
