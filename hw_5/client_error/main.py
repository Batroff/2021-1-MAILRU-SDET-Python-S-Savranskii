import re
from json import dumps
from sys import argv

res = []
with open('../access.log', 'r') as f:
    for line in f:
        if req := re.search('.*HTTP/1.{4}4[0-9]{2}\s[0-9]+', line):
            req_arr = req.group(0).split(' ')
            code = req_arr[-2]
            url = req_arr[6]
            ip = req_arr[0]
            req_len = req_arr[-1]
            res.append((ip, url, req_len, code))

with open('./res.log', 'w+') as f:
    res = sorted(res, reverse=True, key=lambda x: int(x[2]))[:5]
    f.write('\n'.join(f'{ip} {code} {url_len} {url}' for (ip, url, url_len, code) in res))

    f.write('\n')
    if '--json' in argv:
        f.write(f'JSON: {dumps(res)}')

