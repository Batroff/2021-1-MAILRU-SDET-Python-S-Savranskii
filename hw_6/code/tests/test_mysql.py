import pytest

from mysql.builder import MySQLBuilder
from mysql.models import AllRequests, RequestsTypes, MostOften, ClientError, ServerError
from scripts import log_utils


class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.prepare()


class TestAllRequests(MySQLBase):

    def prepare(self):
        self.mysql_builder.create_all_requests(
            description='Requests count',
            count=log_utils.all_requests()
        )

    def test(self):
        resp = self.mysql.session.query(AllRequests).first()
        assert resp.count == 225133


class TestRequestsTypes(MySQLBase):

    def prepare(self):
        self.mysql_builder.create_requests_types(
            requests_types=log_utils.requests_types()
        )

    def test(self):
        resp = self.mysql.session.query(RequestsTypes).all()

        assert {x.method: x.count for x in resp} == {
            'GET': 122095,
            'POST': 102503,
            'HEAD': 528,
            'PUT': 6
        }


class TestMostOften(MySQLBase):

    def prepare(self):
        self.mysql_builder.create_most_often(
            most_often=log_utils.most_often()
        )

    def test(self):
        resp = self.mysql.session.query(MostOften).all()

        assert {x.url: x.count for x in resp} == {
            "/administrator/index.php": 103932,
            "/apache-log/access.log": 26336,
            "/": 6940,
            "/templates/_system/css/general.css": 4980,
            "/robots.txt": 3199,
            "http://almhuette-raith.at/administrator/index.php": 2356,
            "/favicon.ico": 2201,
            "/wp-login.php": 1644,
            "/administrator/": 1563,
            "/templates/jp_hotel/css/template.css": 1287,
        }


class TestClientError(MySQLBase):

    def prepare(self):
        self.mysql_builder.create_client_error(
            client_error=log_utils.client_error()
        )

    def test(self):
        resp = self.mysql.session.query(ClientError).all()

        assert [(x.req_len, x.url) for x in resp] == [
            (1417, '/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53'),
            (1417, '/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53'),
            (1417, '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168'
                   '%3D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA'
                   '.CHARACTER_SETS%29%20END%29%29&Itemid=53'),
            (1417, '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753'
                   '%3D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA'
                   '.CHARACTER_SETS%29%20END%29%29&Itemid=53'),
            (1397, '/index.php?option=com_easyblog&view=dashboard&layout=write'),
        ]


class TestServerError(MySQLBase):

    def prepare(self):
        self.mysql_builder.create_server_error(
            server_error=log_utils.server_error()
        )

    def test(self):
        resp = self.mysql.session.query(ServerError).all()

        assert [(x.ip, x.count) for x in resp] == [
            ('189.217.45.73', 225),
            ('82.193.127.15', 4),
            ('91.210.145.36', 3),
            ('194.87.237.6', 2),
            ('198.38.94.207', 2),
        ]
