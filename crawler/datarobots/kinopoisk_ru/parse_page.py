# coding: utf-8

import re
import os
import datetime
import StringIO

from bs4 import BeautifulSoup
from PIL import Image
from collections import defaultdict
from functools import partial

from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_PERSON_PRODUCER, APP_PERSON_SCRIPTWRITER, APP_FILM_DIRTY_WORDS

from crawler.constants import PAGE_ARCHIVE
from crawler.tor import simple_tor_get_page

from utils.common import traceback_own


YANDEX_KP_ACTORS_TEMPLATE = "http://st.kp.yandex.net/images/actor_iphone/iphone360_{}.jpg"
YANDEX_KP_FILMS_TEMPLATE = "http://st.kp.yandex.net/images/film_big/{}.jpg"
YANDEX_KP_FILMS_SMALL_TEMPLATE = "http://st.kp.yandex.net/images/film/{}.jpg"


class ProbablyBanned(Exception):
    pass


def commatlst(tag):
    return [s.strip() for s in tag.text.strip().split(u',')]


def extract_names_and_ids(tag):
    for atag in tag.find_all('a'):
        if 'name' in atag.attrs['href']:
            yield re.match('[/]name[/](?P<id>[0-9]+)[/]', atag.attrs['href']).groupdict()['id'], atag.text


def extract_countries(tag):
    return [t.text.strip() for t in tag.select('a')]


def date_extract(tag):
    try:
        return datetime.datetime.strptime(tag.select("div.prem_ical")[0].attrs['data-date-premier-start-link'], "%Y%m%d")
    except ValueError:
        try:
            return datetime.datetime.strptime(tag.select("div.prem_ical")[0].attrs['data-date-premier-start-link'], "%Y%m")
        except ValueError:
            return datetime.datetime.strptime(tag.select("div.prem_ical")[0].attrs['data-date-premier-start-link'], "%Y00")


def get_vote(soup):
    csslink = [lnk.attrs['href'] for lnk in soup.find_all('link') if 'votes' in lnk.attrs['href']][0]
    # TODO implement caching

    css = simple_tor_get_page(csslink, tor_flag=True)

    m = re.search('[.]starbar[ ]{width[:][ ](?P<width>[0-9]+)px', css)
    parent_width = float(m.groupdict()['width'])

    starbar_div = soup.select('div.starbar_w')
    child_width = float(dict([i.split(':') for i in starbar_div[0].attrs['style'].split(';')])['width'].replace('px', ''))

    return round(child_width / (parent_width * 10), 2)


def safe_int(item):
    try:
        return int(item)
    except Exception, e:
        return None


def budget(bstring):
    if u'руб.' in bstring:
        #ms = bstring.replace(u'руб.','')
        #There is no way to store rub in database
        print "Encountered budget in RUB. Storing nothing"
        return None
    elif '$' in bstring:
        ms = bstring.replace(u'$', '')
        return safe_int(u''.join(ms.split()))
    else:
        print "Encountered budget in unknown currency.Storing nothing"
        return None


def russian_word(st):
    return bool(re.match(u'[а-я ]+', st.lower().strip()))


def cut_triple_dots(datastringlist):
    for el in datastringlist:
        if not russian_word(el):
            break
        else:
            yield el.strip()


def transform_data_dict(ddict):
    transforms = {
        u'год': lambda d: [('Films',{'year': datetime.datetime.strptime(d.text.strip(),"%Y")})],
        u'страна': lambda d: [('Countries', {'name': c}) for c in extract_countries(d)],
        u'жанр': lambda d: [('Genres', {'name': c}) for c in cut_triple_dots(commatlst(d))],
        u'режиссер': lambda d: [('Persons', {'name':name,'kinopoisk_id':kid, 'p_type': APP_PERSON_DIRECTOR}) for kid,name in extract_names_and_ids(d)],
        u'продюсер': lambda d: [('Persons', {'name':name, 'kinopoisk_id': kid, 'p_type': APP_PERSON_PRODUCER}) for kid,name in extract_names_and_ids(d)],
        u'бюджет': lambda d: [('Films', {'budget': budget(d.text)})],
        u'премьера (мир)': lambda d: [('Films', {'world_release_date': date_extract(d)})],
        u'премьера (РФ)': lambda d: [('Films', {'release_date': date_extract(d)})],
        u'сценарий': lambda d: [('Persons', {'name':name, 'kinopoisk_id': kid, 'p_type': APP_PERSON_SCRIPTWRITER}) for kid,name in extract_names_and_ids(d)],
        u'возраст': lambda d: [('Films', {
            'age_limit': safe_int(
                [e for e in d.parent.select('div.ageLimit')[0].attrs['class']
                 if not e.endswith(u'Limit')][0].split('age')[-1])
        })],
        u'время': lambda d: [('Films', {'duration': safe_int(d.parent.select('td.time')[0].text.split(u'мин.')[0])})]
    }

    transform_keys = transforms.keys()
    for key, val in ddict.items():
        if key in transform_keys:
            for el in transforms[key](val):
                yield el
        else:
            print u"Can't find parser for key: {key}".format(key=key)


def convert_file(input_data):
    fileobj = StringIO.StringIO()
    fileobj.write(input_data)
    fileobj.seek(0)

    img = Image.open(fileobj).convert('RGB')
    conv_file = StringIO.StringIO()
    img.save(conv_file, 'JPEG')
    conv_file.seek(0)

    return conv_file


def get_image(template, actor_id):
    try:
        result = simple_tor_get_page(template.format(actor_id), tor_flag=False)
        return convert_file(result)
    except Exception, e:
        traceback_own(e)

    return None


get_poster = partial(get_image, YANDEX_KP_FILMS_TEMPLATE)
get_small_poster = partial(get_image, YANDEX_KP_FILMS_SMALL_TEMPLATE)
get_photo = partial(get_image, YANDEX_KP_ACTORS_TEMPLATE)


def extract_names(soup):
    nametag = soup.select('h1.moviename-big')[0]
    name = nametag.text.strip()

    for word in APP_FILM_DIRTY_WORDS:
                if word in name:
                    name = name.replace(word, '').strip()

    moviename = ('Films', {'name': name})
    name_orig = soup.find('span', {'itemprop': 'alternativeHeadline'})
    orig_movie_name = ('Films', {
        'name_orig': name_orig.text.strip() if not name_orig is None else ''
    })

    return moviename, orig_movie_name


def actors_wrap(actors_names):
    return [('Persons', {
            'name': value[0],
            'p_type': APP_PERSON_ACTOR,
            'kinopoisk_id': re.match('[/]name[/](?P<id>[0-9]+)[/]', value[1]).groupdict()['id'],
            'p_index': p_index
        }) for p_index, value in enumerate(actors_names, 1) if re.match(u'[а-я ]+', value[0].lower())
    ]


def acquire_page(page_id):
    if not os.path.exists(PAGE_ARCHIVE):
        os.mkdir(PAGE_ARCHIVE)

    page_dump = ''
    dump_path = os.path.join(PAGE_ARCHIVE,str(page_id))
    if os.path.exists(dump_path):
        with open(dump_path) as fd:
            page_dump = fd.read().decode('utf-8')

    if not page_dump:
        url = u"http://www.kinopoisk.ru/film/%d/" % page_id
        res = simple_tor_get_page(url, tor_flag=True)
        page_dump = res.decode('cp1251')

        with open(dump_path, 'w') as fdw:
            fdw.write(page_dump.encode('utf-8'))

    return page_dump


def extract_facts_from_dump(page_dump):
    '''
    Parsing one page from the multiline string @page_dump
    Returns dictionary with keys 'Films', 'Persons', 'Genres'
    '''

    if not page_dump:
        return []

    soup = BeautifulSoup(page_dump)
    info_table = soup.select("div#infoTable")[0]
    tds = info_table.select("td.type")
    data_dict = dict([(f.text.strip(), s) for f, s in [td.parent.select("td") for td in tds]])

    actor_list = soup.find('div', {'id': 'actorList'}).find_all('ul')[0]
    actors_n_l = [(a.text, a.attrs['href']) for a in actor_list.find_all('a')
                  if not 'film' in a.attrs['href']]

    if len(soup.select("div.brand_words")):
        brand_words = ('Films', {'description': soup.select("div.brand_words")[0].text})
    else:
        brand_words = ('Films', {'description': u''})

    movie_name, orig_movie_name = extract_names(soup)
    vote = ('Films', {'rating_kinopoisk': get_vote(soup)})

    facts = []
    facts.extend(transform_data_dict(data_dict))
    facts.extend(actors_wrap(actors_n_l))
    facts.extend([brand_words, movie_name, orig_movie_name, vote])

    list_models = defaultdict(list)
    for element, value in facts:
        list_models[element].append(value)

    return list_models


if __name__ == "__main__":
    d = extract_facts_from_dump(acquire_page(301))
    print d
    for di in d['Films']:
        for k in di:
            print(k)
            print(di[k])

    for di in d['Countries']:
        for k in di:
            print(k)
            print(di[k])
