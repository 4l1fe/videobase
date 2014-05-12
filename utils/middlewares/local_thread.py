# coding: utf-8

import threading

_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_api_request():
    return getattr(_thread_locals, 'api_request', None)

def set_api_request(request):
    _thread_locals.api_request = request

class ThreadLocals(object):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """
    def process_request(self, request):
        _thread_locals.request = request
