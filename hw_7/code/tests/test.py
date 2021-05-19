import pytest

import settings
from mock.flask_mock import SURNAME_DATA
from tests.base import BaseCase

import json

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


class TestMock(BaseCase):

    def add_user(self, name):
        return self.http_client.request(method='POST', location='/add_user', data={'name': f'{name}'})

    def get_user(self, name):
        return self.http_client.request(method='GET', location=f'/get_user/{name}')

    def get_user_surname(self, name):
        return json.loads(self.get_user(name)[-1])['surname']

    def delete_user_surname(self, name):
        return self.http_client.request(method='DELETE', location=f'/delete_user_surname/{name}')

    def update_user_surname(self, name, surname):
        return self.http_client.request(method='PUT', location='/update_user',
                                        data={'name': name, 'surname': surname})

    @pytest.mark.OLD
    def test_get_age(self):
        self.add_user('Vasya')

        user_data = self.get_user('Vasya')

        age = json.loads(user_data[-1])['age']
        assert isinstance(age, int)
        assert 0 <= age <= 100

    @pytest.mark.OLD
    def test_get_surname(self):
        SURNAME_DATA['Olya'] = 'Zaitceva'

        self.add_user('Olya')
        assert self.get_user_surname('Olya') == 'Zaitceva'

    def test_update_surname(self):
        SURNAME_DATA['Kirill'] = 'Zakharov'

        self.add_user('Kirill')
        assert self.get_user_surname('Kirill') == 'Zakharov'

        resp = self.update_user_surname(name='Kirill', surname='Ivanov')
        assert json.loads(resp[-1])['surname'] == 'Ivanov'

    def test_negative_update_surname(self):
        SURNAME_DATA['Morris'] = 'some_name'

        resp = self.update_user_surname(name='Morris', surname='new_name')
        assert resp[-1] == 'User name Morris does not exists'

    def test_delete_surname(self):
        SURNAME_DATA['Ilya'] = 'Odd'

        self.add_user('Ilya')
        assert self.get_user_surname('Ilya') == 'Odd'

        self.delete_user_surname('Ilya')
        assert self.get_user_surname('Ilya') is None
