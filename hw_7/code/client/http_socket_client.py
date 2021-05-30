import logging
import socket
import json

logger = logging.getLogger('requests')


class HttpSocketClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def request(self, method, location, data=None):

        client = self.connect()

        req = '{method} {location} HTTP/1.1\r\n' \
              'Host: {host}\r\n' \
              'Content-Type: application/json\r\n' \
              'Content-Length: {content_len}\r\n' \
              '\r\n' \
              '{data}\r\n'

        content_len = 0
        if data:
            data = json.dumps(data)
            content_len = len(data)

        req_formatted = req.format(method=method, location=location, host=self.host,
                                   content_len=content_len, data=data)

        client.send(req_formatted.encode())
        logger.info(f'Request:\n{req_formatted}')

        resp_data = self.receive(client)
        logger.info(f'Response:\n{resp_data}')
        return resp_data

    @staticmethod
    def receive(client):
        total_data = []

        while True:
            resp_data = client.recv(4096)
            if resp_data:
                total_data.append(resp_data.decode('utf-8'))
            else:
                client.close()
                break

        resp_data = ''.join(total_data).splitlines()
        return resp_data

    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.2)
        client.connect((self.host, self.port))

        return client
