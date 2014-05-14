# coding: utf-8

from bs4 import BeautifulSoup
from django.db import transaction
from apps.films.models import Persons
from crawler.parse_page import crawler_get

headers = {'User-Agent': 'Mozilla/5.0'}


@transaction.commit_on_success
def parse_id_persons(id):
        try:
            response = crawler_get('http://www.kinopoisk.ru/name/' + str(id))
            soup = BeautifulSoup(response.content)
            tag = soup.find('span', attrs={'itemprop': 'alternativeHeadline'})
            person_name = tag.text.strip()
            f = Persons.objects.get(name=person_name)
            f.kinopoisk_id = id
            f.save()
        except Exception:
            pass


parse_id_persons()
