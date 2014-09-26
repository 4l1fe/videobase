# coding: utf-8
""" Поиск новинок на tvzor.ru """
import json
import string

from crawler.tor import simple_tor_get_page

from django.db import connection

HOST = 'http://www.tvzor.ru'
NEW_URL = HOST + '/content_group/50cb2a4ce4b0b8203f880b44/100/0'


def dict_fetch_all(cursor):

    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def parse_tvzor_news():

    # Get page
    page = simple_tor_get_page(NEW_URL)

    # Constant for punctuation
    punctuation = string.punctuation
    trans = string.maketrans(punctuation, ' ' * len(punctuation))

    # String constant
    pattern = '!"#$%&\'()*+,-./:;<=>–№«»?@[\\]^_`{|}~ ' # ascii: 160

    cursor = connection.cursor()

    #Get films from page in json format
    films = json.loads(page)

    news = []
    for film in films:
        try:
            # Film name
            name = film['name'].lower().strip().encode('utf-8').translate(trans)

            # Film year
            year = int(film['releaseDate'])

            query = """SELECT * FROM (SELECT films.name, films.id, EXTRACT(YEAR FROM films.release_date) AS year,
                regexp_split_to_array(trim(both lower(translate(films.name, E%s, %s))), E'\\s+') AS new_name
                FROM films) AS t WHERE t.year=%s AND t.new_name=regexp_split_to_array(%s, E'\\s+')"""

            cursor.execute(query, [pattern, ' ' * len(pattern), year, name])
            result = dict_fetch_all(cursor)

            if len(result) == 1:
                link = HOST + '/movie/' + film['assetId']
                news.append({'film_id': result[0]['id'], 'url': link})

        except Exception, e:
            print e.message

    cursor.close()
    return news