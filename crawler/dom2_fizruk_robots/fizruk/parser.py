#coding: utf-8
from crawler.dom2_fizruk_robots.fizruk.loader import FizrukLoader
import json
from bs4 import BeautifulSoup
from crawler.dom2_fizruk_robots.dom2.parser import get_valid_date_for_str

__author__ = 'vladimir'

fizruk_actors = {

}

class ParseFizruk():
    def __init__(self):
        pass

    @staticmethod
    def parse_all_series():
        all_series_informations = []
        pages = FizrukLoader.get_info_pages()
        for page in pages:
            one_info = ParseFizruk.parse_one_info_page(page)
            all_series_informations = all_series_informations + [one_info]

        return all_series_informations

    @staticmethod
    def parse_one_info_page(page):
        page_info = {
            'label': '',
            'value': '',
            'description': '',
            'date': None
        }
        opened_page = open(page)
        json_page = json.load(opened_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        all = beatiful_soup.find('div', { "id" : "all"})
        content = all.find('div', { "id" : "content"})
        center_block = content.find('div', { "id" : "center-block"})
        date = ParseFizruk.get_date(center_block)
        decription = ParseFizruk.get_description(center_block)
        value = ParseFizruk.get_video_code(center_block)
        caption = ParseFizruk.get_caption(center_block)
        page_info['label'] = caption
        page_info['value'] = value
        page_info['description'] = decription
        page_info['date'] = date
        return page_info

    @staticmethod
    def get_video_code(center_block):
        video_player_now = center_block.find('div', { "id" : "video-player-now"})
        iframe = video_player_now.find('iframe')
        video_link = iframe['src']
        return video_link

    @staticmethod
    def get_date(center_block):
        video_info = center_block.find('div', { "id" : "video-info"})
        left = video_info.find('div', { "class" : "left"})
        a = left.find('a')
        text_date = a.text
        return get_valid_date_for_str(text_date)

    @staticmethod
    def get_description(center_block):
        video_info = center_block.find('div', { "id" : "video-info"})
        left = video_info.find('div', { "class" : "left"})
        v_descr = left.find('div', { "class" : "v_descr"})
        description = v_descr.text
        return description

    @staticmethod
    def get_caption(center_block):
        h1 = center_block.find('h1')
        caption = h1.text
        return caption
