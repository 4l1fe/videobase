# coding: utf-8
from bs4 import BeautifulSoup

from django.utils import timezone
from raven.transport import requests

HOST = 'http://news.sportbox.ru'


def parse_translation():
    date = timezone.now().date() + timezone.timedelta(days=1)
    translations_list = []

    for i in range(1, 4):
        url = HOST + '/video?date={}'.format(date)
        content = requests.get(url).content
        soup = BeautifulSoup(content)

        #Список трансляций на один день
        a_translation = soup.findAll('a', attrs={'class': 'sb_trans_preview_img'})

        for translation in a_translation:
            link = translation.get('href')
            translation_url = HOST + link
            content = requests.get(translation_url).content
            soup = BeautifulSoup(content)

            #Получаем код вставки плеера
            share_link = soup.find('textarea', attrs={'class': 'share_link_content'}).next.prettify()

            name_translation = soup.find('h1', attrs={'itemprop': 'name'}).text

            date_translation = soup.find('h5').text.split()[5].split(':')
            hour = date_translation[0]
            minute = date_translation[1]

            translation_data = {
                'meta': {},
                'title': name_translation,
                'date': timezone.datetime(year=date.year, month=date.month, day=date.day, hour=int(hour),
                                          minute=int(minute)),
                'price': 0,
                'link': translation_url,
                'embed_code': share_link

            }
            translations_list.append(translation_data)

        date = date + timezone.timedelta(days=1)

    return translations_list






