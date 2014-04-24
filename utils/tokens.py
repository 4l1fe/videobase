#coding: utf-8
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


def get_main_token(username='admin', password='admin', host=HOST):
    data = urlencode(dict(username=username, password=password))
    if python_v == 3:
        data = data.encode()
    req = Request(urljoin(host, 'api/v1/auth/login.json'), data)
    resp = urlopen(req)
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


def get_films_persons(sessiom_token, id, host=HOST):
    req = Request(urljoin(host, 'api/v1/films/{}/persons.json'.format(id)))
    req.add_header('Authorization', 'X-VB-Token ' + sessiom_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp


def get_users_persons(session_token, id, host=HOST):
    url = urljoin(host, 'api/v1/users/{}/persons.json'.format(id))
    data = urlencode(dict())  # Для изменения на тип запроса - POST
    req = Request(url, data)
    print(req.get_full_url())
    req.add_header('Authorization', 'X-VB-Token ' + session_token)
    # req.add_header('Authorization', 'Token ' + session_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp


if __name__ == '__main__':
    mt = get_main_token()
    print(mt)
    st = get_session_token(mt)
    print(st)
    resp = get_films_persons(st, 833)
    print(resp)
    resp = get_users_persons(st, 1)
    print(resp)