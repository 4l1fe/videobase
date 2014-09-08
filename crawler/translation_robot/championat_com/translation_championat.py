# coding: utf-8

""" Поиск трансляций championat.com """

import re
from bs4 import BeautifulSoup
from django.utils import timezone

from crawler.tor import simple_tor_get_page

TRANSLATION_URL = 'http://video.championat.com'


def parse_translation_championat_com():
    translation_list = []
    champ_dict = {}

    # Get page
    translation_page = simple_tor_get_page(TRANSLATION_URL)
    soup = BeautifulSoup(translation_page)

    championship_bloc = soup.find('div', {'class': 'video-menu'})

    #Create championship map
    for champ in championship_bloc.find_all('a'):
        try:
            img = champ.find('img')
            if img:
                champ_dict[img.get('src')] = champ.span.text
        except Exception, e:
            print e.message

    translation_table = soup.find('table', {'class': 'table'})

    for trans in translation_table.find_all('tr'):
        try:

            # Get current year
            current_year = timezone.now().year

            # Get title
            title_tag = trans.h3
            title = title_tag.text

            # Get date and time
            dates = trans.find_all('td', {'class': 'date'})
            date = re.findall(ur'\d+', dates[0].text)
            time = re.findall(ur'\d+', dates[1].text)

            #Get price
            price_tag = trans.find('span', {'class': 'button _buy'})
            price = re.search(ur'\d+', price_tag.text).group()

            #Get link
            link = TRANSLATION_URL + title_tag.a.get('href')

            #Get championship
            championship_img = trans.find('img').get('src')
            championship = champ_dict[championship_img]

            #Create dict with information about translation
            translation_data = {
                'title': title,
                'date': timezone.datetime(year=current_year, month=int(date[1]), day=int(date[0]), hour=int(time[0]),
                                          minute=int(time[1])),
                'price': float(price),
                'link': link,
                'meta': {'championship': championship if championship else None},
                'embed_code': None,
            }

            translation_list.append(translation_data)
        except Exception, e:
            print e.message

    return translation_list