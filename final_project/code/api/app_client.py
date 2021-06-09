import json
import os

from api.client import ApiClient


class AppApiClient(ApiClient):

    def add_user(self, username, password, email,
                 method=None, headers=None, cookies=None, expected_status=None):
        if method is None:
            method = "POST"
        if headers is None:
            headers = {"Content-Type": "application/json"}
        if cookies is None:
            cookies = self.session.cookies
        if expected_status is None:
            expected_status = [201]

        data = {
            "username": username,
            "password": password,
            "email": email
        }

        return self._request(method=method, location='api/add_user', headers=headers,
                             data=json.dumps(data), expected_status=expected_status, cookies=cookies)

    def delete_user(self, username, method=None, expected_status=None):
        if method is None:
            method = 'GET'
        if expected_status is None:
            expected_status = [204]

        return self._request(method=method, location=f'api/del_user/{username}', expected_status=expected_status)

    def block_user(self, username, method=None, expected_status=None):
        if method is None:
            method = 'GET'
        if expected_status is None:
            expected_status = [200]

        return self._request(method=method, location=f'api/block_user/{username}', expected_status=expected_status)

    def accept_user(self, username, method=None, expected_status=None):
        if method is None:
            method = 'GET'
        if expected_status is None:
            expected_status = [200]

        return self._request(method=method, location=f'api/accept_user/{username}', expected_status=expected_status)

    def login(self, login, password):
        host = 'localhost'  # test_app
        port = os.environ.get('APP_PORT', '8081')

        headers = {
            'Host': f'{host}:{port}',
            'Origin': f'http://{host}:{port}',
            'Referer': f'http://{host}:{port}/login',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'username': login,
            'password': password,
            'submit': 'Login'
        }

        response = self._request(method='POST', location='login', headers=headers, data=data,
                                 expected_status=[302], allow_redirects=False)

        assert response.headers['Location'] == f'{self.base_url}welcome/'

        self.session.cookies.set("session", response.cookies['session'])
        return {'session': response.cookies['session']}
