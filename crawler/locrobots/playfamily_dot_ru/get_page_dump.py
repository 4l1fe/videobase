# coding: utf-8
'''
Strategies for obtaining page dump from playfamily.ru
'''

from crawler.playfamily_dot_ru.parse_search_page import parse_search_page
from crawler.playfamily_dot_ru.parse_search_page import  form_search_url
from crawler.playfamily_dot_ru.parse_page import parse_page, form_url_from_name


def get_page_urls_parsers(name_orig):
    '''
    Returns list of one or two possible links and parsers
    where information for given film can be found
    on playfamily.ru.
    Parser is function that given page_dump parses it and provides
    information needed
    '''


    url_from_name = form_url_from_name(name_orig)
    search_url = form_search_url(name_orig)
    if url_from_name is None:
        return (search_url,)
    else:
        return ((url_from_name, parse_page), (search_url, parse_search_page))
        