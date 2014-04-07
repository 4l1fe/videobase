'''
Module for emulating browser
'''
from crawler.core.exceptions import RetrievePageException

import requests
from urlparse import urlparse
from os.path import exists
from os.path import join
import os
from collections import namedtuple
import base64
import logging

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


def construct_path(urlstring, kwargs):
    '''
    Constructing correct cache path for urlstring
    '''

    purl = urlparse(urlstring)
    
    if not lexists(purl.netloc):
        os.mkdir(ljoin(purl.netloc))

    repath = u'_'.join(purl.path.split('/'))

    if not lexists(repath):
        os.mkdir(ljoin(repath))

    if 'params' in kwargs or 'query' in kwargs:
        return join(ljoin(repath), base64.urlsafe_b64encode(str(kwargs)))
    else:
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
            try:
                p = u'&'.join( key+u'='+value for key,value in kwargs['params'].items())
                print p
                cachepath = construct_path(url+ p if 'params' in kwargs else '')
            except Exception,e:

                print "Here",e
            if exists(cachepath):
                logging.debug('Found cache for %s in %s. Returning cached copy', url, cachepath)
                with open(cachepath) as fr:
                    fake = FakeResponse(ok=True, content=fr.read(), url=url)
                return fake
            else:
                r = func(url, **kwargs)
                if r.ok:

                    logging.debug("Saving cache for %s in %s.", url, cachepath)

                    with open(cachepath, 'w') as fw:
                        fw.write(r.content)
                return r
        else:
            return func(url, **kwargs)
    return wrapper


def nopage_handler(func):
    def wrapper(url, **kwargs):
        
        r = func(url, **kwargs)
        if r.ok:
            return r
        else:
            raise RetrievePageException(url=url, status_code=r.status_code)
    return wrapper

    
@nopage_handler
@cache
def simple_get(url, **kwargs):
    '''
    Simple wrapper around requests.get function with preset headers
    '''
    return requests.get(url, headers=HEADERS, params=kwargs.get('params', {}))