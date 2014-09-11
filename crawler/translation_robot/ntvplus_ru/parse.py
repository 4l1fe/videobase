# coding: utf-8
from bs4 import BeautifulSoup
from django.utils import timezone
from raven.transport import requests

HOST = 'http://www.ntvplus.ru'

def parse_translation():
    url = HOST + '/online/'
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    items = soup.findAll('tr', {'class': 'daytitle'})

    for item in items:
        date = item.text
        if date == u'Сегодня':
            date = timezone.now().date()

        elif date == u'Завтра':
            date = timezone.now().date() + timezone.timedelta(days=1)
        else:
            date = date

        categories = item.get('class')


    print items

