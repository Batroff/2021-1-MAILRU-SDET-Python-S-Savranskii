import random

import pytest

from test_ui.base import BaseCase
from faker import Faker
from re import sub

fake = Faker()


class TestRegister(BaseCase):
    """
    Тесты:
     - длина логина len < 6 || len > 16
     - длина почты > 64
     - длина пароля len > 255
     - несовпадающие пароли
     - одинаковые (логины, почты, пароли) у разных пользователей
     - чекбокс
     - неправильный email
     - корректная регистрация
    """

    def prepare(self):
        self.register_page = self.auth_page.go_to_register_page()

    @staticmethod
    def generate_user():
        return {
            'username': fake.lexify('?' * random.randint(6, 16)),
            'password': fake.password(),
            'email': fake.email()
        }

    @pytest.mark.parametrize("invalid_user,expected_err", [
        ({"username": fake.lexify('?' * 5)}, "Incorrect username length"),
        ({"username": fake.lexify('?' * 20)}, "Incorrect username length"),
        ({"email": fake.lexify('?' * 64) + '@test.ru'}, "Incorrect email length"),
        ({"email": f"{fake.lexify('?')}@{fake.lexify('?')}.{fake.lexify('?')}"}, "Incorrect email length"),
        pytest.param({"password": fake.password(length=256)}, "Incorrect password length", marks=pytest.mark.BUG)
    ], ids=[
        "username_short",
        "username_long",
        "email_short",
        "email_long",
        "password_long"
    ])
    @pytest.mark.UI
    def test_input_data_len_negative(self, invalid_user, expected_err):
        user = self.generate_user()
        username = invalid_user.get("username", user['username'])
        email = invalid_user.get("email", user['email'])
        password = invalid_user.get("password", user['password'])

        self.register_page.register(username=username,
                                    email=email,
                                    password=password,
                                    confirm_password=password,
                                    checkbox=True,
                                    get_home_page=False)

        query_users = self.mysql.select_user_by_name(user['username'])
        assert len(query_users) == 0

        assert self.register_page.is_reg_error_exists(expected_err)

    @pytest.mark.UI
    def test_different_confirm_password(self):
        user = self.generate_user()
        password = fake.password(length=5)
        confirm_password = fake.password(length=6)

        self.register_page.register(username=user['username'],
                                    email=user['email'],
                                    password=password,
                                    confirm_password=confirm_password,
                                    checkbox=True,
                                    get_home_page=False)

        query_users = self.mysql.select_user_by_name(user['username'])
        assert len(query_users) == 0

        assert self.register_page.is_reg_error_exists('Passwords must match')

    @pytest.mark.UI
    @pytest.mark.BUG
    def test_create_user_with_existing_password(self):
        user = self.mysql_builder.create_user()

        new_user = self.generate_user()
        self.register_page.register(username=new_user['username'],
                                    email=new_user['email'],
                                    password=user.password,
                                    confirm_password=user.password,
                                    checkbox=True)

        query_users = self.mysql.select_user_by_name(new_user['username'])
        assert len(query_users) == 1

    @pytest.mark.UI
    def test_create_user_with_existing_name(self):
        user = self.mysql_builder.create_user()

        new_user = self.generate_user()
        self.register_page.register(username=user.username,
                                    email=new_user['email'],
                                    password=new_user['password'],
                                    confirm_password=new_user['password'],
                                    checkbox=True,
                                    get_home_page=False)

        query_users = self.mysql.select_user_by_name(user.username)
        assert len(query_users) == 1, f"Expected 1 user in db with username '{user.username}'"

        assert self.auth_page.is_login_error_exists('User already exist')

    @pytest.mark.UI
    @pytest.mark.BUG
    def test_create_user_with_existing_email(self):
        user = self.mysql_builder.create_user()

        new_user = self.generate_user()
        self.register_page.register(username=new_user['username'],
                                    email=user.email,
                                    password=new_user['password'],
                                    confirm_password=new_user['password'],
                                    checkbox=True,
                                    get_home_page=False)

        query_users = self.mysql.select_user_by_email(user.email)
        assert len(query_users) == 1, f"Expected 1 user in db with email '{user.email}'"

        assert self.auth_page.is_login_error_exists('User already exist')

    @pytest.mark.parametrize("email,expected_err", [
        (sub(r'\..*', '.', fake.email()), "Invalid email address"),
        (sub(r'@.*\.', '@.', fake.email()), "Invalid email address"),
        (fake.email().split('.')[0], "Invalid email address"),
        (f'{fake.lexify("@???-??.???")}', "Invalid email address"),
        (fake.email().replace('@', ''), "Invalid email address"),
    ], ids=[
        "Invalid domain",
        "Invalid domain",
        "Without domain",
        "Without email name",
        "Without 'at' symbol"
    ])
    @pytest.mark.UI
    def test_create_user_incorrect_email(self, email, expected_err):
        user = self.generate_user()

        self.register_page.register(username=user['username'],
                                    email=email,
                                    password=user['password'],
                                    confirm_password=user['password'],
                                    checkbox=True,
                                    get_home_page=False)

        query_users = self.mysql.select_user_by_email(email)
        assert len(query_users) == 0, f"Expected 0 users in db with email '{email}'"

        assert self.auth_page.is_login_error_exists(expected_err), f"Expected error '{expected_err}'"

    @pytest.mark.UI
    @pytest.mark.BUG
    def test_create_user_correct(self):
        user = self.generate_user()

        self.register_page.register(username=user['username'],
                                    email=user['email'],
                                    password=user['password'],
                                    confirm_password=user['password'],
                                    checkbox=True)

        username = user['username']
        query_users = self.mysql.select_user_by_name(username)
        assert len(query_users) == 1, f"Expected 1 user in db with username '{username}'"

        user = query_users[0]
        access, active, start_time = user[-3], user[-2], user[-1]
        assert access == 1, f"Expected 'access' in state 1"
        assert active == 1, f"Expected 'active' in state 1"
        assert start_time is not None, f"Expected 'start_active_time' not NULL"
