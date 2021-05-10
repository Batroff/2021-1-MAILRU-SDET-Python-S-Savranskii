import os
import re


def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def all_requests():
    with open(os.path.join(repo_root(), 'assets', 'access.log'), 'r') as f:
        lines_quantity = sum(1 for _ in f)

    return lines_quantity


def requests_types():
    requests = dict()
    with open(os.path.join(repo_root(), 'assets', 'access.log'), 'r') as f:
        for line in f:
            if res := re.search('"[A-Z]+.*HTTP/1.{2}\"', line):
                method = res.group(0).split(' ')[0][1:]
                requests[method] = requests.get(method, 0) + 1

    return requests


def most_often():
    urls = dict()
    with open(os.path.join(repo_root(), 'assets', 'access.log'), 'r') as f:
        for line in f:
            if req := re.search('.*HTTP/1.{4}[0-9]{3}', line):
                url = req.group(0).split(' ')[6]
                urls[url] = urls.get(url, 0) + 1

    return sorted(urls.items(), reverse=True, key=lambda kv: kv[1])[:10]


def client_error():
    res = []
    with open(os.path.join(repo_root(), 'assets', 'access.log'), 'r') as f:
        for line in f:
            if req := re.search('.*HTTP/1.{4}4[0-9]{2}\\s[0-9]+', line):
                req_arr = req.group(0).split(' ')
                code = req_arr[-2]
                url = req_arr[6]
                ip = req_arr[0]
                req_len = req_arr[-1]
                res.append((ip, url, req_len, code))

    return sorted(res, reverse=True, key=lambda x: int(x[2]))[:5]


def server_error():
    popular_ip = dict()
    with open(os.path.join(repo_root(), 'assets', 'access.log'), 'r') as f:
        for line in f:
            if re.search('\".*HTTP/1.{4}5[0-9]{2}', line):
                ip = re.search('^(([0-9]{1,3}\\.){3}[0-9]{1,3})', line).group(0)
                popular_ip[ip] = popular_ip.get(ip, 0) + 1

    return sorted(popular_ip.items(), reverse=True, key=lambda x: x[1])[:5]
