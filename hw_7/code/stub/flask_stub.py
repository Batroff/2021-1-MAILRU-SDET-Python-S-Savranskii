import json
import os
import random

from flask import Flask

app = Flask(__name__)


@app.route('/get_age/<name>', methods=['GET'])
def get_user_id_by_name(name):
    return json.dumps(random.randint(0, 100)), 200


if __name__ == '__main__':
    host = os.environ.get('STUB_HOST', '127.0.0.1')
    port = os.environ.get('STUB_PORT', '8090')

    app.run(host, port)
