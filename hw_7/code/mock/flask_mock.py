import json
import logging
import os
import threading

from flask import Flask, request

import settings

SURNAME_DATA = {}

app = Flask(__name__)
logging.basicConfig(filename=os.path.join('/tmp', 'mock.log'), level=logging.INFO)


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    if SURNAME_DATA.get(name):
        del SURNAME_DATA[name]
        return json.dumps(f'Surname for user {name} deleted'), 200

    return f'Surname for user {name} not found', 404


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return json.dumps(surname), 200

    return f'Surname for user {name} not found', 404


@app.route('/update_surname/<name>', methods=['PUT'])
def put_user_surname(name):
    if SURNAME_DATA.get(name):
        surname = json.loads(request.data)['surname']
        SURNAME_DATA['name'] = surname
        return json.dumps({'name': name, 'surname': surname}), 201

    return f'Surname for user {name} not found', 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()

    return json.dumps(f'OK, exiting'), 200