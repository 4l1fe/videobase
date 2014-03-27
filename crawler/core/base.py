# coding: utf-8

class BaseParser(object):
    pass


class BaseLoad(object):
    def __init__(self, host, url, params):
        self.host = ''
        self.url = url
        self.params = params

    def load(self, load_function):
        response = load_function(self.url, self.params)
        return response