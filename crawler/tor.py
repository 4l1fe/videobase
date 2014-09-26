# coding: utf-8
import re
import requests
import time
import pycurl
import socket
import cStringIO as StringIO

from crawler.constants import TOR_PROXY, TOR_RECONNECTS
from crawler.utils.headers import get_random_weighted_browser_string
from videobase.settings import USE_THOR

DEFAULT_HEADERS = [ 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset: UTF-8',
        ]


########################################################################
def renew_connection(passAuth="mypassword"):
    s = socket.socket()
    try:
        s.connect(('127.0.0.1', 9051))

        s.send('AUTHENTICATE "{0}"\r\n'.format(passAuth))
        resp = s.recv(1024)

        if resp.startswith('250'):
            s.send("signal NEWNYM\r\n")
            resp = s.recv(1024)

            if resp.startswith('250'):
                print "Identity renewed"
                return True
            else:
                print "response 2:", resp
        else:
            print "response 1:", resp

    except Exception, e:
        print "Can't renew identity: ", e

    finally:
        s.close()

    time.sleep(2)

    return False


########################################################################
def get_page(url, user_agent, headers=DEFAULT_HEADERS):
    # Init Data
    flag = False

    # Init IO
    retrieved_body = StringIO.StringIO()
    retrieved_headers = StringIO.StringIO()

    # Init curl
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.HEADER, False)
    curl.setopt(pycurl.ENCODING, 'gzip,deflate')
    curl.setopt(pycurl.SSL_VERIFYPEER, False)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.MAXREDIRS, 2)
    curl.setopt(pycurl.TIMEOUT, 80)
    curl.setopt(pycurl.VERBOSE, 0)
    curl.setopt(pycurl.FAILONERROR, 1)
    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    curl.setopt(pycurl.PROXY, TOR_PROXY)
    curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.write)
    curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.write)

    try:
        flag = True
        curl.perform()
    except Exception, e:
        #return e
        pass
    finally:
        if flag:
            body, header = retrieved_body.getvalue(), retrieved_headers.getvalue()

        curl.close()
        retrieved_body.close()
        retrieved_headers.close()

    return body, header


########################################################################
def check_result(header):
    parse_header = re.findall(r"(?P<name>.*?): (?P<value>.*?)", header)
    if 'Location' in dict(parse_header).keys():
        return False

    return True


def get_page_or_renew(url, user_agent, tor_flag):
    counter = 0
    if tor_flag:
        while counter < TOR_RECONNECTS:
            body, header = get_page(url, user_agent)

            if not check_result(header):
                print check_result(header)
                renew_connection()
                counter += 1
            else:
                return body
    else:
        return requests.get(url).content


def simple_tor_get_page(url, tor_flag=False):
    header = get_random_weighted_browser_string()
    return get_page_or_renew(url, header, tor_flag and USE_THOR)

########################################################################
def main():
    # Init Data
    counter = 0

    url = 'http://www.kinopoisk.ru/film/751952'

    headers = DEFAULT_HEADERS
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.4) Gecko/2008102920 AdCentriaIM/1.7 Firefox/3.0.4"

    while counter < 10:
        body, header = get_page(url, user_agent, headers)

        if not check_result(header):
            renew_connection()
            counter += 1
        else:
            print body
            break


if __name__ == '__main__':
    main()
