# coding: utf-8

""" Поиск новинок на now.ru и stream.ru """

import re
import string
from bs4 import BeautifulSoup

from django.db import connection

from crawler.tor import simple_tor_get_page
from utils.common import dict_fetch_all


NOW_HOST = 'http://www.now.ru'
STREAM_HOST = 'http://www.stream.ru'
NOW_NEW_URL = NOW_HOST + '/index/belt?filter_type=category&filter_value=movies&filter_parent=movies&query_type=new'
ROBOT_NOW = 'now_ru'
STREAM_NEW_URL = STREAM_HOST + '/films/?sort_by=publication_date'
ROBOT_STREAM = 'stream_ru'

SITE_DICT = {
    ROBOT_NOW: {
        'host': NOW_HOST,
        'news_url': NOW_NEW_URL,
        'films_tag_args': ('figcaption',),
        'name_tag_args': ('p', {'class': 'car-par-name'}),
        'year_tag_args': ('p', {'class': 'car-par-year'})
    },
    ROBOT_STREAM: {
        'host': STREAM_HOST,
        'news_url': STREAM_NEW_URL,
        'films_tag_args': ('li', {'class': 'item'}),
        'name_tag_args': ('a', {'class': 'title'}),
        'year_tag_args': ('p', {'class': 'genre-year'})
    },
}


def parse_news(robot_name):

    #Get site
    site = SITE_DICT[robot_name]

    # Get page
    page = simple_tor_get_page(site['news_url'])
    soup = BeautifulSoup(page)

    # Constant for punctuation
    punctuation = string.punctuation
    trans = string.maketrans(punctuation, ' ' * len(punctuation))

    # String constant
    pattern = '!"#$%&\'()*+,-./:;<=>–№«»?@[\\]^_`{|}~ ' # ascii: 160

    cursor = connection.cursor()

    #Get films from page
    films = soup.find_all(*site['films_tag_args'])

    news = []
    for film in films:
        try:
            # Find name from tag
            name_tag = film.find(*site['name_tag_args'])
            name = name_tag.text.lower().strip().encode('utf-8').translate(trans)

            # Find year from tag
            year_tag = film.find(*site['year_tag_args'])
            year = int(re.search(ur'\d+', year_tag.text).group())

            query = """SELECT * FROM (SELECT films.name, films.id, EXTRACT(YEAR FROM films.release_date) AS year,
                regexp_split_to_array(trim(both lower(translate(films.name, E%s, %s))), E'\\s+') AS new_name
                FROM films) AS t WHERE t.year=%s AND t.new_name=regexp_split_to_array(%s, E'\\s+')"""

            cursor.execute(query, [pattern, ' ' * len(pattern), year, name])
            result = dict_fetch_all(cursor)

            if len(result) == 1:
                link_tag = name_tag if robot_name == ROBOT_STREAM else name_tag.a

                link = site['host'] + link_tag.get('href')
                news.append({'film_id': result[0]['id'], 'url': link})

        except Exception, e:
            print e.message

    cursor.close()
    return news
