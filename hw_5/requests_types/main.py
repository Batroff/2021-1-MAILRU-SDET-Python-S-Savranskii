import re
from sys import argv
from json import dumps

requests = dict()
with open('../access.log', 'r') as f:
    for line in f:
        if res := re.search('"[A-Z]+.*HTTP/1.{2}\"', line):
            method = res.group(0).split(' ')[0][1:]
            requests[method] = requests.get(method, 0) + 1

with open('./res.log', 'w+') as f:
    res = {k: v for (k, v) in requests.items() if v != 0}
    f.write(', '.join([f'{k} -- {v}' for (k, v) in res.items()]))

    f.write('\n')
    if '--json' in argv:
        f.write(f'JSON: {dumps(res)}')

