'''
Module for emulating browser
'''
import requests
from urlparse import urlparse
from os.path import exists
from os.path import join
import os
from collections import namedtuple
import base64

FakeResponse = namedtuple('FakeResponse', ['ok', 'content', 'url'])

HEADERS = {'User-Agent': 'Mozilla/5.0'}

CACHE_DIR = './cache'




def ljoin(p):
    '''
    Return path with prepended CACHE_DIR
    '''
    return join(CACHE_DIR, p)

def lexists(p):
    '''
    Rerurns path with prependended CACHE_DIR
    '''
    return exists(ljoin(p))

if not lexists(''):
    os.mkdir(ljoin(''))

def construct_path(urlstring):
    '''
    Constructing correct cache path for urlstring
    '''

    purl = urlparse(urlstring)

    if not lexists(purl.netloc):
        os.mkdir(ljoin(purl.netloc))

    repath = '_'.join(purl.path.split('/'))

    if not lexists(repath):
        os.mkdir(ljoin(repath))

    if purl.query == '':
        return join(ljoin(repath), 'cache')
    else:
        return join(ljoin(repath), base64.urlsafe_b64encode(purl.query))


def cache(func):
    '''
    Caching wrapper for get functions
    '''
    def wrapper(url, **kwargs):
        '''
        Wrapper function
        '''

        if (not 'cache' in kwargs) or kwargs['cache']:
            cachepath = construct_path(url)
            if exists(cachepath):
                with open(cachepath) as fr:
                    fake = FakeResponse(ok=True, content=fr.read(), url=url)
                return fake
            else:
                r = func(url)
                with open(cachepath, 'w') as fw:
                    fw.write(r.content)
                return r
    return wrapper


@cache
def simple_get(url, encoding=None):
    '''
    Simple wrapper around requests.get function with preset headers

    '''
    return requests.get(url, headers=HEADERS)



    