#coding: utf-8
__author__ = 'vladimir'


def convert_to_unicode(s):
    res = u''
    if isinstance(s, str):
        res = s.decode('utf-8')
    if isinstance(s, unicode):
        res = s
    return res


