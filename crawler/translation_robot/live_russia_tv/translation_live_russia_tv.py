# coding: utf-8

""" Поиск трансляций live.russia.tv """

import re
from bs4 import BeautifulSoup
from django.utils import timezone
from pytz import timezone as pytz_timezone
from crawler.tor import simple_tor_get_page

TRANSLATION_URL = 'http://live.russia.tv'
PLAYER_LINK = 'http://player.rutv.ru/iframe/live/id/%s/showZoomBtn/false/isPlay/true/'
MONTHS = {
    u'января': 1,
    u'февраля': 2,
    u'марта': 3,
    u'апреля': 4,
    u'мая': 5,
    u'июня': 6,
    u'июля': 7,
    u'августа': 8,
    u'сентября': 9,
    u'октября': 10,
    u'ноября': 11,
    u'декабря': 12,
}

TZ = pytz_timezone('Europe/Moscow')


def parse_translation_live_russia_tv():
    translation_list = []

    # Get current date
    current_date = timezone.now()

    # Get page
    translation_page = simple_tor_get_page(TRANSLATION_URL)
    soup = BeautifulSoup(translation_page)

    translation_bloc = soup.find('div', {'class': ['broadcasts', 'tab-non-active', 'tab-broadcasts']})

    for trans in translation_bloc.find_all('li'):
        try:

            # Get date and time
            time_tag = trans.find('div', {'class': 'time'})
            time = re.findall(ur'\d+', time_tag.text)
            date_tag = trans.find('div', {'class': 'label'})
            date_str = date_tag.text.lower().strip().split()

            if len(date_str) == 1:
                if date_str[0] == u'сегодня':
                    date = timezone.datetime(year=current_date.year, month=current_date.month, day=current_date.day,
                                         hour=int(time[0]), minute=int(time[1]), tzinfo=TZ)
            elif len(date_str) == 3:
                date = timezone.datetime(year=int(date_str[2]), month=MONTHS[date_str[1]], day=int(date_str[0]),
                                         hour=int(time[0]), minute=int(time[1]), tzinfo=TZ)
            else:
                continue

            # Get title
            title_tag = trans.h2
            title = title_tag.text

            #Get link
            href = trans.a.get('href')
            link = TRANSLATION_URL + href

            #Get video id
            video_id = href.split('/')[-1]

            #Create dict with information about translation
            translation_data = {
                'title': title,
                'date': date,
                'price': float(0),
                'link': link,
                'meta': {},
                'embed_code': None,
                'value': video_id,
                'player': PLAYER_LINK % video_id
            }

            translation_list.append(translation_data)
        except Exception, e:
            print e.message

    return translation_list

