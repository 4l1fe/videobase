# coding: utf-8
from bs4 import BeautifulSoup
from django.utils import timezone
import requests

HOST = 'http://www.ntvplus.ru'
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


def parse_ntv_plus_translation():
    url = HOST + '/online/'
    content = requests.get(url).content
    soup = BeautifulSoup(content)

    items = soup.findAll('td', {'class': 'name'})
    translations_list = []

    for item in items:

        link = item.a.get('href')
        translation_url = url + link
        try:
            content = requests.get(translation_url).content
        except Exception:
            continue
        soup = BeautifulSoup(content)
        date_text = soup.find('div', {'class': 'timeblock'}).text
        temp = date_text.split()

        if temp[0].lower() == u'сегодня':
            date = timezone.now().date()
            date = format_date(date, date_text)

        elif temp[0].lower() == u'завтра':
            date = timezone.now().date() + timezone.timedelta(days=1)
            date = format_date(date, date_text)

        else:
            temp = date_text.split(',')

            try:
                temp = temp[1].split()
            except IndexError:
                continue

            day = int(temp[0])
            month = MONTHS[temp[1].lower()]
            temp = temp[3].split(':')
            hour = int(temp[0])
            minute = int(temp[1])

            date = timezone.datetime(year=timezone.now().year, month=month, day=day,
                                         hour=hour, minute=minute)

        name_translation = soup.findAll('h1')[1].text
        type = soup.find('span', {'class': 'caption'}).text
        quality = soup.findAll('span', {'class': 'comment'})
        if quality.__len__() == 2:
            quality = quality[1].text
            price = soup.findAll('div', {'class': 'ppvprice'})[1].text
        else:
            quality = quality[0].text
            price = soup.findAll('div', {'class': 'ppvprice'})[0].text

        price = price.split()
        price = float(price[0])

        meta = {
            'type': type,
            'quality': quality,
        }

        translation_data = {
                'title': name_translation,
                'date': date,
                'price': price,
                'link': translation_url,
                'meta': meta,
                'embed_code': ' ',
                'value': '',
                'player': None
        }

        translations_list.append(translation_data)
    return translations_list


def format_date(date, date_text):
        date = timezone.datetime(year=date.year, month=date.month, day=date.day)

        temp = date_text.split()
        temp = temp[2]
        temp = temp.split(':')
        hour = int(temp[0])
        minute = int(temp[1])

        date = date + timezone.timedelta(hours=hour, minutes=minute)

        return date







