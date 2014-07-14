# coding: utf-8
'''
Kinopoisk robot
'''
import re
import os
import time
import datetime
import StringIO

from bs4 import BeautifulSoup
from PIL import Image
from collections import defaultdict
from functools import partial

from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_PERSON_PRODUCER, APP_PERSON_SCRIPTWRITER
from crawler.constants import PAGE_ARCHIVE
from crawler.tor import simple_tor_get_page


YANDEX_KP_ACTORS_TEMPLATE = "http://st.kp.yandex.net/images/actor_iphone/iphone360_{}.jpg"
YANDEX_KP_FILMS_TEMPLATE = "http://st.kp.yandex.net/images/film_big/{}.jpg"


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
    return datetime.datetime.strptime(tag.select("div.prem_ical")[0].attrs['data-date-premier-start-link'], "%Y%m%d")


def get_vote(soup):
    csslink = [lnk.attrs['href'] for lnk in soup.find_all('link') if 'votes' in lnk.attrs['href']][0]
    # TODO implement caching

    r = simple_tor_get_page(csslink, tor_flag=True)

    css = r
    m = re.search('[.]starbar[ ]{width[:][ ](?P<width>[0-9]+)px', css)
    parent_width = float(m.groupdict()['width'])

    starbar_div = soup.select('div.starbar_w')
    child_width = float(dict([i.split(':') for i in starbar_div[0].attrs['style'].split(';')])['width'].replace('px',''))

    return round(child_width/parent_width*10, 2)


def budget(bstring):
    if u'руб.' in bstring:
        #ms = bstring.replace(u'руб.','')
        #There is no way to store rub in database
        print "Encountered budget in RUB. Storing nothing"
        return None
    elif '$' in bstring:
        ms = bstring.replace(u'$', '')
        return int(u''.join(ms.split()))
    else:
        print "Encountered budget in unknown currency.Storing nothing"
        return None

def russian_word(st):
    return bool(re.match(u'[а-я ]+',st.lower().strip()))
        
def cut_triple_dots(datastringlist):
    for el in datastringlist:
        if russian_word(el):
            break
        else:
            yield el.strip()

def transform_data_dict(ddict):
    transforms = {
        #u'roд': lambda d: ('Films',{'freleasedate': datetime.datetime.strptime(d.text.strip(),"%Y%m%d")}),
        u'страна': lambda d: [('Countries', {'name': c}) for c in extract_countries(d)],
        u'жанр': lambda d: [('Genres', {'name': c}) for c in cut_triple_dots(commatlst(d))],
        u'режиссер': lambda d: [('Persons', {'name':name,'kinopoisk_id':kid, 'p_type': APP_PERSON_DIRECTOR}) for kid,name in extract_names_and_ids(d)],
        u'продюсер': lambda d: [('Persons', {'name':name, 'kinopoisk_id': kid, 'p_type': APP_PERSON_PRODUCER}) for kid,name in extract_names_and_ids(d)],
        u'бюджет': lambda d: [('Films', {'fbudget': budget(d.text)})],
        u'премьера (мир)': lambda d: [('Films', {'frelease_date': date_extract(d)})],
        u'премьера (РФ)': lambda d: [('Films', {'frelease_date': date_extract(d)})],
        u'сценарий': lambda d: [('Persons', {'name':name, 'kinopoisk_id': kid, 'p_type': APP_PERSON_SCRIPTWRITER}) for kid,name in extract_names_and_ids(d)],
        u'возраст': lambda d: [('Films', {'age_limit': int(
            [e for e in d.parent.select('div.ageLimit')[0].attrs['class']
             if not e.endswith(u'Limit')][0].split('age')[-1])
        })],
        u'время': lambda d :[('Films', {'fduration': int( d.parent.select('td.time')[0].text.split(u'мин.')[0])})]
    }
    tkeys = transforms.keys()
    for key, val in ddict.items():
        if key in tkeys:
            for el in transforms[key](val):
                yield el
        else:
            print u"Can't find parser for {}".format(key)


def get_image(template, actor_id):
    try:
        r = simple_tor_get_page(template.format(actor_id), tor_flag=True)
        fileobj = StringIO.StringIO()
        fileobj.write(r)
        fileobj.seek(0)
        img = Image.open(fileobj).convert('RGB')
        conv_file = StringIO.StringIO()
        img.save(conv_file, 'JPEG')
        conv_file.seek(0)
        return conv_file
    except Exception as e:
        print e
        return None

get_poster = partial(get_image, YANDEX_KP_FILMS_TEMPLATE)
get_photo = partial(get_image, YANDEX_KP_ACTORS_TEMPLATE)


def extract_names(soup):
    nametag = soup.select('h1.moviename-big')[0]
    moviename = ('Films', {'name': nametag.text.strip()})
    orig_movie_name = ('Films', {'name_orig': nametag.select('span')[0].text.strip() if len(nametag.select('span')) else ''})
    return moviename, orig_movie_name


def actors_wrap(actors_names):
    return [('Persons', {'name': an, 'p_type': APP_PERSON_ACTOR, 'kinopoisk_id': re.match('[/]name[/](?P<id>[0-9]+)[/]', ai).groupdict()['id']}) for an, ai in actors_names if re.match(u'[а-я ]+',an.lower(),)]


def acquire_page(page_id):
    if not os.path.exists(PAGE_ARCHIVE):
        os.mkdir(PAGE_ARCHIVE)

    dump_path = os.path.join(PAGE_ARCHIVE,str(page_id))
    if os.path.exists(dump_path):
        with open(dump_path) as fd:
            page_dump = fd.read().decode('utf-8')
    else:
        url =u"http://www.kinopoisk.ru/film/%d/" % page_id
        res = simple_tor_get_page(url, tor_flag=True)
        page_dump = res.decode('cp1251')
        with open(dump_path, 'w') as fdw:
            fdw.write(page_dump.encode('utf-8'))

    return page_dump


def extract_facts_from_dump(page_dump):
    '''
    Parsing one page from the multiline string @page_dump
    Returns
    Dictionary with keys 'Films', 'Persons', 'Genres'
    '''

    facts = []
    soup = BeautifulSoup(page_dump)
    info_table = soup.select("div#infoTable")[0]
    tds = info_table.select("td.type")
    data_dict = dict([(f.text.strip(), s) for f, s in [td.parent.select("td") for td in tds]])

    actor_list = soup.select("div#actorList")[0]
    actors_n_l = [(a.text, a.attrs['href']) for a in actor_list.find_all('a') if  not 'film' in a.attrs['href']]

    brand_words = ('Films', {'description': soup.select("div.brand_words")[0].text})

    moviename, orig_movie_name = extract_names(soup)
    vote = ('Films', {'rating_kinopoisk': get_vote(soup)})

    facts.extend(transform_data_dict(data_dict))
    facts.extend(actors_wrap(actors_n_l))
    facts.extend([brand_words, moviename, orig_movie_name, vote])

    ddict = defaultdict(list)

    for pd in facts:
        element, value = pd
        ddict[element].append(value)
    return ddict


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


