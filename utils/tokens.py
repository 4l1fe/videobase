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


HOST = 'http://vsevi.com'


def get_main_token(host=HOST, username='admin', password='admin'):
    data = urlencode(dict(username=username, password=password))
    if python_v == 3:
        data = data.encode()
    resp = urlopen(urljoin(host, 'api/v1/auth/login.json'), data=data)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp['token']


def get_session_token(main_token, host=HOST):
    req = Request(urljoin(host, 'api/v1/auth/session.json'))
    req.add_header('Authorization', 'Token ' + main_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp['session_token']


if __name__ == '__main__':
    mt = get_main_token()
    print(mt)
    st = get_session_token(mt)
    print(st)