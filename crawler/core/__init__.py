# coding: utf-8
import requests
from collections import namedtuple
import os
import logging

headers = {'User-Agent': 'Mozilla/5.0'}

Request = namedtuple('Request',['content','ok','status'])


def cache_requests(domain,filename_generator, protocol ='http://'):
    def decorator(func):
        def wrapper (key):
            root = os.path.join('./cache',domain)
            if not os.path.exists(root):
                os.mkdir(root)

            cache_path = os.path.join(root,filename_generator(key))
            if os.path.exists(cache_path):
                with open(cache_path) as cachefile:
                    data = cachefile.read()
            else:
                req = func(protocol+domain+key)
                with open(cache_path,'w') as cachefile:
                    cachefile.write(req.content)



def get_page(url):
    return requests.get(url, headers = headers)

