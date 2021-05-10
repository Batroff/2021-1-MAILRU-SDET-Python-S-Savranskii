from faker import Faker

from mysql.models import AllRequests, RequestsTypes, MostOften, ClientError, ServerError

fake = Faker()


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_all_requests(self, description, count):
        result = AllRequests(
            description=description,
            count=count
        )
        self.client.session.add(result)

        return result

    def create_requests_types(self, requests_types: dict):
        result = [RequestsTypes(method=k, count=v) for (k, v) in requests_types.items()]
        self.client.session.add_all(result)

        return result

    def create_most_often(self, most_often: dict):
        result = [MostOften(url=url, count=count) for (url, count) in most_often]
        self.client.session.add_all(result)

        return result

    def create_client_error(self, client_error: list):
        result = [ClientError(ip=ip, url=url, req_len=req_len, code=code) for (ip, url, req_len, code) in client_error]
        self.client.session.add_all(result)

        return result

    def create_server_error(self, server_error: list):
        result = [ServerError(ip=ip, count=count) for (ip, count) in server_error]
        self.client.session.add_all(result)

        return result
