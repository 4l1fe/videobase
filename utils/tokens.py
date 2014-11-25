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


def get_main_token(username, password, address):
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


def get_session_token(main_token, address):
    req = Request(urljoin(address, 'api/v1/auth/session.json'))
    req.add_header('X-MI-TOKEN', main_token)
    resp = urlopen(req)
    resp_data = resp.read()
    if python_v == 3:
        resp_data = resp_data.decode()
    json_resp = json.loads(resp_data)
    return json_resp['session_token']


def add_friendship(main_token, session_token, id_, address):
    req = Request(urljoin(address, 'api/v1/users/{}/friendship.json'.format(id_)), data="{'id': 3455}")
    req.add_header('X-MI-SESSION', session_token)
    req.add_header('X-MI-TOKEN', main_token)
    resp = urlopen(req)
    return resp.read()


def del_friendship(session_token, id_, host):
    import httplib
    cl = httplib.HTTPConnection(host)
    headers = {'X-MI-SESSION': session_token}
    cl.request('DELETE', '/api/v1/users/{}/friendship.json'.format(id_), headers=headers)
    resp = cl.getresponse()
    return resp.read()


def upload_avatar(main_token, session_token,  address):
    import requests
    cookies = {'x-session': session_token, 'x-token': main_token}
    data = {'username': 'from_post_method', }
    resp = requests.post(address+'/profile/', files={'avatar': open('avatar.jpg', 'rb')}, cookies=cookies)
    return resp


def casts_chats_msgs(session_token, id_, **kwargs):
    url = 'api/v1/castschats/{}/msgs.json'.format(id_)
    if kwargs:
        url = url + '?' + urlencode(kwargs)
    req = Request(urljoin(address, url))
    req.add_header('X-MI-SESSION', session_token)
    resp = urlopen(req)
    return resp.read()


def casts_chats_view(main_token, session_token, id_):
    import requests
    url = 'casts/{}/'.format(id_)
    resp = requests.get(urljoin(address, url), cookies={'x-token': main_token, 'x-session':session_token})
    return resp.content


def casts_chats_users(main_token, session_token, id_):
    url = 'api/v1/castschats/{}/users.json'.format(id_)
    req = Request(urljoin(address, url))
    req.add_header('X-MI-TOKEN', main_token)
    req.add_header('X-MI-SESSION', session_token)
    resp = urlopen(req)
    return resp.read()


if __name__ == '__main__':
    host = 'vsevi.com'
    address = 'http://{}'.format(host)
    mt = get_main_token('test@test.test', 'test', address)
    print(mt)
    st = get_session_token(mt, address)
    print(st)
    from pprint import pprint as pp
    import json
    # resp = casts_chats_msgs(st, 329, limit=1)
    # pp(json.loads(resp))
    # resp = casts_chats_view(mt, st, 329)
    # print(resp)
    # resp = casts_chats_users(mt, st, 329)
    resp = add_friendship(mt, st, 8, address)
    print(resp)