# coding: utf-8
import os

RATING_GZIP_FILE_URL = "http://ftp.sunet.se/pub/tv+movies/imdb/ratings.list.gz"
PAGE_ARCHIVE = './page_dumps/'
SUPERVISOR_XMLRPC = 'http://localhost:9001/RPC2'
TOR_PROXY = '127.0.0.1:9050'
USE_TOR = True
# This option is void if USE_TOR is True
USE_SOCKS5_PROXY = False
SOCKS5_PROXY_ADDRESS = 'socks5://127.0.0.1:5555'
TOR_RECONNECTS = 100
BROWSER_STRINGS_FILE = os.path.join(os.path.dirname(__file__), 'browsers.txt')

browser_freq = {
    "Internet Explorer": 24.3,
    "Firefox": 42.9,
    "Chrome": 24.6,
    "Safari": 4.1,
    "Opera": 2.6
}

with open(BROWSER_STRINGS_FILE) as bf:
    browser_strings = list(s.strip() for s in bf.readlines())



        


