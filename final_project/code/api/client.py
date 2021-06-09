import logging
import socket
import requests

from urllib.parse import urljoin

logger = logging.getLogger('pytest')


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

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

        assert response.status_code in expected_status, \
            ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"! '
                                        f'Expected status codes: {" ".join(map(lambda x: str(x), expected_status))}.')

        if jsonify:
            return response.json()

        return response

    @staticmethod
    def _log_post_request(url, response):
        logger.info(f'Response from {url}\n'
                    f'\tcode: {response.status_code}\n'
                    f'\theaders: {response.headers}\n'
                    f'\tcookies: {response.cookies}\n'
                    f'\ttext: {response.text}\n\n')

    @staticmethod
    def _log_pre_request(method, url, headers, data, files, cookies, expected_status, allow_redirects):
        ip = socket.gethostbyname(socket.gethostname())
        logger.info(f'{ip} -- {method} request for {url}\n'
                    f'\tExpected status code = {expected_status}, allow redirects = {allow_redirects}\n'
                    f'\theaders = {headers}\n'
                    f'\tdata = {data}\n'
                    f'\tcookies = {cookies}\n'
                    f'\tfiles = {files}\n\n')
