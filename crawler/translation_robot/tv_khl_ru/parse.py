# coding: utf-8
from bs4 import BeautifulSoup
import re
import datetime
import requests

__author__ = 'vladimir'

MAIN_SITE_LINK = 'http://video.khl.ru'

class TvKHLRuParser():
    def __init__(self):
        pass

    @staticmethod
    def get_price_from_string(str_price):
        currrency_price = re.split('\s+', str_price, flags=re.UNICODE)[1]
        digit_price = float(currrency_price.replace(',','.'))
        return int(digit_price)

    @staticmethod
    def get_time(item_div):
        item_desc__tag = item_div.find('div', {"class": "item-desc"})
        time_tag = item_desc__tag.find('span', {"class": "date"})
        times = time_tag.getText().split(',')
        t_date = datetime.datetime.strptime(times[0], '%d.%m.%Y')
        t_time = datetime.datetime.strptime(times[1].replace(" ", ""), '%H:%M')
        result = datetime.datetime.combine(t_date, t_time.time())
        if result:
            return result
        else:
            return None

    @staticmethod
    def get_title(item_div):
        a_tag = item_div.find('a', {"class": "vs"})
        divs = a_tag.findAll('div')
        title = divs[0].find('img')['title'] + ' - ' + divs[1].find('img')['title']
        if title:
            return title
        else:
            ''

    @staticmethod
    def get_link(item_div):
        a_tag = item_div.find('a', {"class": "vs"})
        link = MAIN_SITE_LINK + a_tag['href']
        if link:
            return link
        else:
            return ''

    @staticmethod
    def get_price(item_div):
        item_desc_tag = item_div.find('div', {"class": "item-desc"})
        cost_tag = item_desc_tag.find('a', {"class": "buy-transl-link"})
        price = TvKHLRuParser.get_price_from_string(cost_tag.contents[0])
        if price:
            return price
        else:
            return 0

    @staticmethod
    def get_items_list_div():
        site_link = MAIN_SITE_LINK + '/main'
        response = requests.get(site_link)
        beatiful_soup = BeautifulSoup(response.content)
        main_container_div = beatiful_soup.find('div',{ "class" : "main-container"})
        main_wrap_div = main_container_div.find('div',{ "class" : "main-wrap"})
        main_div = main_wrap_div.find('div',{ "class" : "main"})
        wrapper_div = main_div.find('div',{ "class" : "wrapper"})
        announce_div = wrapper_div.find('div',{ "class" : "announce"})
        items = announce_div.findAll('div',{ "class" : "item"})
        return items

    @staticmethod
    def get_info_for_one_item(one_item_div):
        streams = []
        time = TvKHLRuParser.get_time(one_item_div)
        title = TvKHLRuParser.get_title(one_item_div)
        price = TvKHLRuParser.get_price(one_item_div)
        link = TvKHLRuParser.get_link(one_item_div)
        one_stream = {
            'date': time,
            'price': price,
            'title': title,
            'link': link,
            'meta': {},
            'embed_code': None,
            'value': None,
            'player': None
        }

        streams.append(one_stream)
        return streams

    @staticmethod
    def get_translations():
        items_list = TvKHLRuParser.get_items_list_div()
        all_streams = []
        for item_div in items_list:
            if item_div:
                streams = TvKHLRuParser.get_info_for_one_item(item_div)
                all_streams = all_streams + streams

        return all_streams


def parse_khl():
    return TvKHLRuParser.get_translations()

