import json
import os

import requests
from flask import Flask, request

app = Flask(__name__)
app_data = {}
user_id_seq = 1


@app.route('/add_user', methods=['POST'])
def add_user():
    global user_id_seq

    user_name = json.loads(request.data)['name']
    if user_name not in app_data:
        app_data[user_name] = user_id_seq

        data = {'user_id': user_id_seq}
        user_id_seq += 1
        return json.dumps(data), 201
    else:
        return f'User name {user_name} already exists: id {app_data[user_name]}', 400


@app.route('/update_user', methods=['PUT'])
def update_user_surname():
    global user_id_seq

    user_name = json.loads(request.data)['name']
    user_surname = json.loads(request.data)['surname']

    mock_host = os.environ['MOCK_HOST']
    mock_port = os.environ['MOCK_PORT']

    if user_name in app_data:
        resp = requests.put(url=f'http://{mock_host}:{mock_port}/update_surname/{user_name}',
                            data=json.dumps({'surname': user_surname}))

        return resp.json(), resp.status_code
    else:
        return f'User name {user_name} does not exists', 404


@app.route('/delete_user_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    mock_host = os.environ['MOCK_HOST']
    mock_port = os.environ['MOCK_PORT']

    if app_data.get(name):
        resp = requests.delete(url=f'http://{mock_host}:{mock_port}/delete_surname/{name}')
        return resp.json(), resp.status_code
    else:
        return f'User name {name} does not exists', 404


@app.route('/get_user/<name>', methods=['GET'])
def get_user_by_name(name):
    if user_id := app_data.get(name):
        stub_host = os.environ['STUB_HOST']
        stub_port = os.environ['STUB_PORT']

        age = None
        try:
            age = requests.get(f'http://{stub_host}:{stub_port}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system:\n{e}')

        mock_host = os.environ['MOCK_HOST']
        mock_port = os.environ['MOCK_PORT']

        surname = None
        try:
            resp = requests.get(f'http://{mock_host}:{mock_port}/get_surname/{name}')
            if resp.status_code == 200:
                surname = resp.json()

        except Exception as e:
            print(f'Unable to get surname from external system:\n{e}')

        data = {'user_id': user_id,
                'age': age,
                'surname': surname
                }

        return json.dumps(data), 200
    else:
        return f'User name {name} not found', 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8080')

    app.run(host, port)
