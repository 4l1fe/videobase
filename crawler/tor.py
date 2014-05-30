# coding: utf-8

import re
import pycurl
import socket
import cStringIO as StringIO


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

    return False


########################################################################
def get_page(url, useragent, headers):
    flag = False
    curl = pycurl.Curl()
    retrieved_body = StringIO.StringIO()
    retrieved_headers = StringIO.StringIO()

    try:
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HTTPHEADER, headers)
        curl.setopt(pycurl.HEADER, False)
        curl.setopt(pycurl.ENCODING, 'gzip,deflate')
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        curl.setopt(pycurl.FOLLOWLOCATION, True)
        curl.setopt(pycurl.USERAGENT, useragent)
        curl.setopt(pycurl.MAXREDIRS, 2)
        curl.setopt(pycurl.TIMEOUT, 80)
        curl.setopt(pycurl.VERBOSE, 2)
        curl.setopt(pycurl.FAILONERROR, 1)
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        curl.setopt(pycurl.PROXY, '127.0.0.1:9050')
        curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.write)
        curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.write)
        curl.perform()

        flag = True
    except Exception, e:
        return e

    finally:
        curl.close()

        if flag:
            body, header = retrieved_body.getvalue(), retrieved_headers.getvalue()

        retrieved_body.close()
        retrieved_headers.close()

    return body, header


########################################################################
def check_result(header):
    parse_header = re.findall(r"(?P<name>.*?): (?P<value>.*?)", header)
    if 'Location' in dict(parse_header).keys():
        return False

    return True


########################################################################
def main():
    # Init Data
    counter = 0

    url = 'http://www.kinopoisk.ru/film/751952'
    # url = 'http://www.kinopoisk.ru/handler_trailer_popup.php?ids=301'

    headers = [
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset: UTF-8',
    ]

    useragent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.4) Gecko/2008102920 AdCentriaIM/1.7 Firefox/3.0.4"

    while counter < 10:
        body, header = get_page(url, useragent, headers)

        if not check_result(header):
            renew_connection()
            counter += 1
        else:
            print body
            break


if __name__ == '__main__':
    main()
