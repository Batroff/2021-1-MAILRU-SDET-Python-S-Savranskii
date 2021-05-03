import re
from sys import argv
from json import dumps

urls = dict()
with open('../access.log', 'r') as f:
    for line in f:
        if req := re.search('.*HTTP/1.{4}[0-9]{3}', line):
            url = req.group(0).split(' ')[6]
            urls[url] = urls.get(url, 0) + 1

with open('./res.log', 'w+') as f:
    res = sorted(urls.items(), reverse=True, key=lambda kv: kv[1])[:10]
    f.write('\n'.join([f'{k} -- {v}' for (k, v) in res]))

    f.write('\n')
    if '--json' in argv:
        f.write(f'JSON: {dumps(res)}')

