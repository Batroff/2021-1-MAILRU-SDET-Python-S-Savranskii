import json
import os

import flask
from flask import Flask, request

app = Flask(__name__)

users = {}
mysql = None


@app.route('/is_alive', methods=['GET'])
def is_ready():
    return json.dumps({'status': 'ready'}), 200


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    response = flask.Response()
    response.headers['Content-Type'] = 'application/json'

    if username in users.keys():
        response.response = json.dumps({'vk_id': users[username]})
        response.status_code = 200

    else:
        response.status_code = 404
        response.response = json.dumps({})

    return response


@app.route('/vk_id_add', methods=['POST'])
def vk_id_add():
    response = flask.Response()

    data = json.loads(request.data)
    username = data['username']
    vk_id = data['vk_id']

    if username is None or vk_id is None:
        response.response = json.dumps({'error': f'bad data provided'})
        response.status_code = 400

    elif username in users.keys():
        response.response = json.dumps({'error': f'{username} is already exists'})
        response.status_code = 304

    else:
        users[username] = vk_id
        response.response = json.dumps({'status': 'success'})
        response.status_code = 201

    return response, 200


if __name__ == '__main__':
    host = os.environ.get('MOCK_HOST', '0.0.0.0')
    port = os.environ.get('MOCK_PORT', '8090')

    app.run(host, port)
