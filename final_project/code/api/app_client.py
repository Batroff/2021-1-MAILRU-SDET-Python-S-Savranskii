import os

from api.client import ApiClient


class AppApiClient(ApiClient):

    def login(self, login, password):
        host = 'localhost'  # test_app
        port = os.environ.get('APP_PORT', '8081')

        headers = {
            'Host': f'{host}:{port}',
            'Origin': f'http://{host}:{port}',
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

        return {'session': response.cookies['session']}
