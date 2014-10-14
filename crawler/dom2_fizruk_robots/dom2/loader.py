# coding: utf-8
from bs4 import BeautifulSoup
import requests
from crawler.locrobots.save_util import save_loaded_data_to_file

__author__ = 'vladimir'

URL_LOAD = 'http://dom2.ru/videos/page/{}'
URL_OLD_ACTRORS_LOAD = 'http://dom2.ru/heroes/old/page/{}'


# Загрузка страници с dom2.ru
class Dom2Loader():
    def __init__(self):
        pass

    @staticmethod
    def load_pages():
        pages = []
        page_index = 0
        while True:
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
        if len(beatiful_soup.findAll('div', { "class" : "item first"})) > 0 or len(beatiful_soup.findAll('div', {"id": "movieContainer"}))>0 \
                or len(beatiful_soup.findAll('div', { "class" : "phtgal"})) > 0:
            return {'html': page_content, 'url': page_link}
        else:
            return None

    @staticmethod
    def actors_generate_json(page_content, page_link):
        beatiful_soup = BeautifulSoup(page_content)
        if len(beatiful_soup.findAll('td',{"class": "descr"})) > 0:
            return {'html': page_content, 'url': page_link}
        else:
            return None


    @staticmethod
    def load_video_info_page(link, label):
        file_name = None
        response = requests.get(link)
        prepared_json = Dom2Loader.generate_json(response.content, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, u'video_info_page_{}'.format(label), 'dom2')
        return file_name

    @staticmethod
    def load_old_actors_pages():
        pages = []
        page_index = 0
        while True:
            page_file = Dom2Loader.load_one_old_actors_pages(page_index)
            if not page_file:
                break
            page_index += 1
            pages = pages + [page_file]
        return pages

    @staticmethod
    def load_current_actors_page():
        file_name = None
        page_link = 'http://dom2.ru/heroes'
        response = requests.get(page_link)
        prepared_json = Dom2Loader.actors_generate_json(response.content, page_link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'page_current_actors', 'dom2')
        return file_name

    @staticmethod
    def load_one_old_actors_pages(page_index):
        file_name = None
        page_link = URL_OLD_ACTRORS_LOAD.format(page_index)
        response = requests.get(page_link)
        prepared_json = Dom2Loader.actors_generate_json(response.content, page_link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'page_old_actors_{}'.format(page_index), 'dom2')
        return file_name