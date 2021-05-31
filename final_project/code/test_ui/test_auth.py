from faker import Faker

from test_ui.base import BaseCase

fake = Faker()


class TestAuthUsername(BaseCase):
    """
    Тесты:
     - негативный на длину логина
     - на корректный логин с доступом 1
     - на корректный логин с доступом 0
     - на неправильный логин
    """

    def test_username_length_negative(self):
        username = fake.lexify('????')
        password = fake.bothify('#?#?#?#?')

        self.auth_page.login(login=username, password=password, get_home_page=False)

        assert self.auth_page.is_login_error_exists('Incorrect username length')

    def test_correct_login(self):
        user_with_access = self.mysql_builder.create_user()
        username, password = user_with_access.username, user_with_access.password

        home_page = self.auth_page.login(login=username, password=password)

        assert home_page.is_opened()

    def test_login_without_access(self):
        user_without_access = self.mysql_builder.create_user(access=0)
        username, password = user_without_access.username, user_without_access.password

        self.auth_page.login(login=username, password=password, get_home_page=False)

        assert self.auth_page.is_login_error_exists('Ваша учетная запись заблокирована')

    def test_wrong_data_login(self):
        username = fake.lexify('??????')
        password = fake.bothify('#?#?#?#?')

        self.auth_page.login(login=username, password=password, get_home_page=False)

        assert self.auth_page.is_login_error_exists('Invalid username or password')
