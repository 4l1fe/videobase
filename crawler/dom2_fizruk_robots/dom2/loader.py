# coding: utf-8
from bs4 import BeautifulSoup
import requests
from crawler.locrobots.save_util import save_loaded_data_to_file

__author__ = 'vladimir'

URL_LOAD = 'http://dom2.ru/videos/page/{}'


# Загрузка страници с dom2.ru
class Dom2Loader():
    def __init__(self):
        pass

    @staticmethod
    def load_pages():
        pages = []
        page_index = 0
        while True:
            print page_index
            page_file = Dom2Loader.load_one_page(page_index)
            if not page_file:
                break
            page_index += 1
            pages = pages + [page_file]
        return pages

    @staticmethod
    def load_one_page(page_index):
        file_name = None
        page_link = URL_LOAD.format(page_index)
        response = requests.get(page_link)
        prepared_json = Dom2Loader.generate_json(response.content, page_link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'page_{}'.format(page_index), 'dom2')
        return file_name

    @staticmethod
    def generate_json(page_content, page_link):
        beatiful_soup = BeautifulSoup(page_content)
        if len(beatiful_soup.findAll('div', { "class" : "item first"}))>0:
            return {'html': page_content, 'url': page_link}
        else:
            return None