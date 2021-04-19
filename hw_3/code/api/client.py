import logging
from urllib.parse import urljoin

import allure
import requests
import faker


class ResponseStatusCodeException(Exception):
    pass


logger = logging.getLogger('test')


class ApiClient:
    cookies = {
        'ssdc': '',
        'mc': '',
        'sdcs': '',
        'csrftoken': '',
    }

    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def get_csrf(self):
        headers = {
            'Connection': 'keep-alive',
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/dashboard',
        }
        response = self._request('GET', location='csrf/', headers=headers, cookies=self.cookies)
        self.cookies['csrftoken'] = response.cookies.get('csrftoken')

    @allure.step('Login in...')
    def post_login(self, email, password, success_url, fail_url):
        data = {
            'email': email,
            'password': password,
            'continue': success_url,
            'failure': fail_url,
        }
        headers = {
            'Host': 'auth-ac.my.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/',
        }
        url = 'https://auth-ac.my.com/auth'
        response = self._request(method='POST', url=url, headers=headers, data=data, allow_redirects=False,
                                 expected_status=[302])

        # Auth cookies
        self.cookies['ssdc'] = response.cookies['ssdc']
        self.cookies['mc'] = response.cookies['mc']

        response = self._request('GET', url=response.headers['Location'], headers={
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/',
        }, cookies=self.cookies, allow_redirects=False, expected_status=[302])

        response = self._request('GET', url=response.headers['Location'], headers={
            'Host': 'auth-ac.my.com',
            'Referer': 'https://target.my.com/',
        }, cookies=self.cookies, allow_redirects=False, expected_status=[302])

        # Get sdcs cookie
        response = self._request('GET', url=response.headers['Location'], headers={
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/',
        }, cookies=self.cookies, allow_redirects=False, expected_status=[302])
        self.cookies['sdcs'] = response.cookies.get('sdcs')

        # Get continue page
        response = self._request('GET', url=response.headers['Location'], headers={
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/',
        }, cookies=self.cookies, allow_redirects=False)

        self.get_csrf()

        assert response.url == success_url, f'Got {response.url} instead of {success_url}'

    def _request(self, method, location=None, url=None, headers=None, data=None, cookies=None, files=None, params=None,
                 jsonify=False, json=None, allow_redirects=True, expected_status=None):

        if expected_status is None:
            expected_status = [200]
        if url is None and location is not None:
            url = urljoin(self.base_url, location)
        else:
            url = url

        self._log_pre_request(method, url, headers, data, files, cookies, expected_status, allow_redirects)
        response = self.session.request(method, url, headers=headers, data=data, cookies=cookies,
                                        files=files, params=params, json=json,
                                        allow_redirects=allow_redirects)
        self._log_post_request(url, response)

        if response.status_code not in expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            return response.json()

        return response

    @staticmethod
    def _log_post_request(url, response):
        logger.info(f'Response from {url}: \n'
                    f'\tcode: {response.status_code}\n'
                    f'\theaders: {response.headers}\n'
                    f'\tcookies: {response.cookies}\n')

    @staticmethod
    def _log_pre_request(method, url, headers, data, files, cookies, expected_status, allow_redirects):
        logger.info(f'{method} request for {url}.\n'
                    f'\tExpected status code = {expected_status}, allow redirects = {allow_redirects}.\n'
                    f'\theaders = {headers}.\n'
                    f'\tdata = {data}.\n'
                    f'\tcookies = {cookies}.\n'
                    f'\tfiles = {files}.\n')
