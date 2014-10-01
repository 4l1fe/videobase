# coding: utf-8
import json
from bs4 import BeautifulSoup
from crawler.dom2_fizruk_robots.dom2.loader import Dom2Loader

__author__ = 'vladimir'

#episode = один день


class ParseDom2():
    def __init__(self):
        pass

    @staticmethod
    def parse_pages():
        pages = Dom2Loader.load_pages()
        for page in pages:
            ParseDom2.parse_one_page(page)

    @staticmethod
    def parse_one_page(page):
        opned_page = open(page)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        ParseDom2.get_episods_for_page(beatiful_soup)
        episods = ParseDom2.get_episods_for_page(beatiful_soup)
        for episode in episods:
            episod_quick_info = ParseDom2.get_episode_quick_info(episode)
            ParseDom2.parse_one_episode(episod_quick_info)

    @staticmethod
    def get_episods_for_page(soup):
        main = soup.find('table', {"class": "all"})
        middle_td = main.find('td', {"class": "middle"})
        table = middle_td.find('table', {"class": "bottom-bg"})
        div = table.find('div', {"class": "content max-width"})
        div_content = div.find('div', {"id": "the_content"})
        div_the_content2 = div_content.find('div', {"id": "the_content2"})
        inner_table = div_the_content2.find('table', {"class": "center-content"})
        left_column = inner_table.find('td', {"class": "left-column"})
        div_persent_pad = left_column.find('div', {"class": "percent-pad"})
        center_table = div_persent_pad.find('table', {"class": "center-subcontent"})
        left_slice = center_table.find('td', {"class": "left-slice"})
        div_big_panel = left_slice.find('div', {"class": "b-bigPanel"})
        div_big_panel_content = div_big_panel.find('div', {"class": "b-bigPanel__content"})
        div_photos = div_big_panel_content.find('div', {"class": "photos"})
        div_items = div_photos.findAll('div', {"class": "item first"})
        div_items = div_items + div_photos.findAll('div', {"class": "item "})
        return div_items

    @staticmethod
    def parse_one_episode(link):
        pass

    @staticmethod
    def get_episode_quick_info(episode):
        pass


    @staticmethod
    def get_all_videos_for_episode():
        pass

    @staticmethod
    def parse_video_page():
        pass

    @staticmethod
    def parse_actors_for_episode(episode_date):
        pass