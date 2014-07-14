# coding: utf-8
import re

class HTML_with_type(unicode):
    page_type =None

def rub_to_int(rub_price):
    '''
    Get int value from string like '79 руб.'

    '''
    return int(next(re.finditer('([0-9]+)',rub_price)).groups()[0])


def utfdecode(func):
    '''
    Decorator for checking if data is unicode string and decoding it to unicode
    from utf8 str
    '''
    def wrapper(page_str):
        '''
        Wrapper function
        '''
        if type(page_str) is HTML_with_type:
            return func(page_str)
        elif type(page_str) is str:
            decoded = page_str.decode('utf-8')
            return func(decoded)
        elif type(page_str) is unicode:
            return func(page_str)
        else:
            raise NameError('Wrong type of argument! str or unicode expected')

    return wrapper
