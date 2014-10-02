# coding: utf-8
import json
import os
import urllib2
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
        quick_info = {
            'label': '',
            'video_link': '',
            'poster': '',
        }

        a_tag = episode.find('a', {"class": "imgBox link no-select"})

        quick_info['label'] = episode.find('div', {"class": "photo-list-title"}).find('a').contents[0]
        quick_info['video_link'] = 'http://dom2.ru'+a_tag['href']
        poster_link = a_tag.find('img')['src']
        quick_info['poster'] = ParseDom2.save_poster_to_file(poster_link, quick_info['label'])
        print '#', quick_info['label']
        print quick_info['video_link']
        print quick_info['poster']
        return quick_info

    @staticmethod
    def get_all_videos_for_episode():
        pass

    @staticmethod
    def parse_video_page():
        pass

    @staticmethod
    def parse_actors_for_episode(episode_date):
        pass

    @staticmethod
    def save_poster_to_file(link, name):
        file_name = None
        directory = 'static/upload/dom2'
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            if 'dom2' not in link:
                link = 'http://dom2.ru'+link
            img = urllib2.urlopen(link)
            with open(directory + '/' + name + '.jpg', 'wb') as localFile:
                localFile.write(img.read())
            file_name = name + '.jpg'
        except Exception, e:
            print e.message
            print "Poster saving failed"
        return file_name