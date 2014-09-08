from bs4 import BeautifulSoup

from django.utils import timezone
from raven.transport import requests

HOST = 'http://news.sportbox.ru'

def parse_translation():
    date = timezone.now().date().t
    # date = datetime.datetime.now().date()
    url = HOST + '/video?date={}'.format(date)
    translations = []
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    a_translation = soup.findAll('a', attrs={'class': 'sb_trans_preview_img'})
    for translation in a_translation:
        link = translation.get('href')
        translation_url = HOST + link
        content = requests.get(translation_url).content
        soup = BeautifulSoup(content)
        link_translation = soup.find('textarea', attrs={'class': 'share_link_content'}).next
        name_translation = soup.find('h1', attrs={'itemprop': 'name'}).text
        date_translation = soup.find('h5')



        print link

    print soup



