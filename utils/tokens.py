#coding: utf-8
"""Содержит пару удобных методов для получения токенов по клиентским запросам через urllib.
"""

import sys
import json

python_v = sys.version_info[0]

if python_v == 2:
    from urllib2 import urlopen, Request
    from urllib import urlencode
    from urlparse import urljoin
elif python_v == 3:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode, urljoin


HOST = 'localvsevi'
ADDR = 'http://{}'.format(HOST)


def get_main_token(username, password, address=ADDR):
    data = urlencode(dict(username=username, password=password))
    if python_v == 3:
        data = data.encode()
    req = Request(urljoin(address, 'api/v1/auth/login.json'), data)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp['X-MI-TOKEN']


def get_session_token(main_token, address=ADDR):
    req = Request(urljoin(address, 'api/v1/auth/session.json'))
    req.add_header('X-MI-TOKEN', main_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp['session_token']


if __name__ == '__main__':
    mt = get_main_token(username='ak@aaysm.com', password='akka')
    print(mt)
    st = get_session_token(mt)
    print(st)