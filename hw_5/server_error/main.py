import re
from sys import argv
from json import dumps

popular_ip = dict()
with open('../access.log', 'r') as f:
    for line in f:
        if req := re.search('\".*HTTP/1.{4}5[0-9]{2}', line):
            code = req.group(0)[-3:]
            ip = re.search('^(([0-9]{1,3}\.){3}[0-9]{1,3})', line).group(0)
            popular_ip[ip] = popular_ip.get(ip, 0) + 1

with open('./res.log', 'w+') as f:
    res = sorted(popular_ip.items(), reverse=True, key=lambda x: x[1])[:5]
    f.write('\n'.join(f'{ctr} -- {ip}' for (ip, ctr) in res))

    f.write('\n')
    if '--json' in argv:
        f.write(f'JSON: {dumps(res)}')

