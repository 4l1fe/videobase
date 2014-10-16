#coding: utf-8
from bs4 import BeautifulSoup
import requests
from crawler.locrobots.save_util import save_loaded_data_to_file

__author__ = 'vladimir'

URL_LOAD = 'http://fizruk.tnt-online.ru/video.html'


class FizrukLoader():
    def __init__(self):
        pass

    @staticmethod
    def get_info_pages():
        pages = []
        response = requests.get(URL_LOAD)
        beatiful_soup = BeautifulSoup(response.content)
        tvbl_s = beatiful_soup.findAll('div', { "class" : "tvbl"})
        for one_tvbl in tvbl_s:
            text = one_tvbl.find('div', { "class" : "text"})
            h4 = text.find('h4')
            a = h4.find('a')
            label = a.text
            link = 'http://fizruk.tnt-online.ru/' + a['href']
            info_page_response = requests.get(link)
            prepared_json = FizrukLoader.generate_json(info_page_response.content, link)
            if prepared_json:
                file_name = save_loaded_data_to_file(prepared_json, label, 'fizruk')
                pages = pages + [file_name]
        return pages

    @staticmethod
    def generate_json(page_content, page_link):
        return {'html': page_content, 'url': page_link}
