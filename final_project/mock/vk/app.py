import json
import os
import random

import flask
from flask import Flask

from mysql_client import MysqlClient

app = Flask(__name__)

users = {}


@app.route('/is_alive', methods=['GET'])
def is_ready():
    return json.dumps({'state': 'ready'}), 200


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    response = flask.Response()
    response.headers['Content-Type'] = 'application/json'

    if username in users.keys():
        response.response = json.dumps({'vk_id': users[username]})
        response.status_code = 200

        return response

    else:
        mysql = MysqlClient('test_qa', 'qa_test', 'test_db')
        mysql.connect()
        query = mysql.select_user_by_name(username)
        mysql.connection.close()

        if len(query) == 1:
            users[username] = str(random.randint(1000, 10000))
            response.response = json.dumps({'vk_id': users[username]})
            response.status_code = 200

            return response

    response.status_code = 404
    response.response = json.dumps({})
    return response


if __name__ == '__main__':
    host = os.environ.get('MOCK_HOST', '0.0.0.0')
    port = os.environ.get('MOCK_PORT', '8090')

    app.run(host, port)
