#coding: utf-8
"""Содержит пару удобных методов для получения токенов по клиентским запросам через urllib.
Так же есть методы на просмотрт возвращаемых значений от API проекта.
"""

import sys
import json
from pprint import pprint as pp
import httplib

python_v = sys.version_info[0]

if python_v == 2:
    from urllib2 import urlopen, Request
    from urllib import urlencode
    from urlparse import urljoin
elif python_v == 3:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode, urljoin


HOST = 'http://dmitriy-book.com'
# HOST = 'http://127.0.0.1:9000'


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
    return json_resp['X-MI-TOKEN']


def get_session_token(main_token, host=HOST):
    req = Request(urljoin(host, 'api/v1/auth/session.json'))
    req.add_header('X-MI-TOKEN', main_token)
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


def get_users_persons(session_token, id, page=1, per_page=10, type_='all', host=HOST):
    url = urljoin(host, 'api/v1/users/{}/persons.json'.format(id))
    data = urlencode(dict(page=page, per_page=per_page, type=type_))
    req = Request(url, data)
    req.add_header('Authorization', 'X-VB-Token ' + session_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp


def get_person(session_token, id_, meth, extend=False, host=HOST):
    req = Request(urljoin(host, 'api/v1/persons/{}.json'.format(id_)))
    if meth.lower() == 'post':
        data = urlencode(dict(extend=extend))
        req.add_data(data)
    req.add_header('Authorization', 'X-VB-Token ' + session_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp


def get_person_films(id_, meth, page=1, per_page=12, type_='a', host=HOST):
    data = urlencode(dict(page=page, per_page=per_page, type_=type_))
    if meth.lower() == 'post':
        req = Request(urljoin(host, 'api/v1/persons/{}/filmography.json'.format(id_)))
        req.add_data(data)
    else:
        req = Request(urljoin(host, 'api/v1/persons/{}/filmography.json?'.format(id_)))

    # req.add_header('Authorization', 'X-VB-Token ' + session_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp


def film_unsubscribe(session_token, id_, host=HOST):
    cl = httplib.HTTPConnection(host)
    headers = {'X-MI-SESSION': session_token}
    cl.request('DELETE', '/api/v1/films/{}/action/subscribe.json'.format(id_), headers=headers)
    resp = cl.getresponse()
    return resp.read()



if __name__ == '__main__':
    mt = get_main_token(username='nana@nana.na', password='nana')
    print(mt)
    st = get_session_token(mt)
    print(st)
    # resp = get_films_persons(st, 3)
    # pp(resp)
    # resp = get_users_persons(st, 1, 1, 10)
    # pp(resp)
    # resp = get_person(st, 12, 'get')
    # pp(resp)
    # resp = get_person(st, 12, 'post')
    # pp(resp)
    # resp = get_person(st, 12, 'post', extend=True)
    # pp(resp)
    # resp = get_person_films(2, 'get')
    # pp(resp)
    resp = film_unsubscribe(st, 71)
    pp(resp)
