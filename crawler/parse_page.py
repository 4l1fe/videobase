# coding: utf-8
'''
Stage 1

1.1 collecting all data from page film

1.2 Refreshing and building all possible films, Persons, PersonFilms, finding persons without poster

1.3 Downloading poster, and posters for persons, updating Persons and film


'''

import re
import requests
from bs4 import BeautifulSoup
import datetime
import pprint
from collections import defaultdict
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_PERSON_PRODUCER
import StringIO
from PIL import Image

YANDEX_KP_ACTORS_TEMPLATE = "http://st.kp.yandex.net/images/actor_iphone/iphone360_{}.jpg"


headers = {'User-Agent': 'Mozilla/5.0'}

def commatlst(tag):
    return tag.text.strip().split(u',')

def date_extract(tag):
    return datetime.datetime.strptime(tag.select("div.prem_ical")[0].attrs['data-date-premier-start-link'],"%Y%m%d")


def get_vote(soup):
    csslink =[ lnk.attrs['href'] for lnk in soup.find_all('link') if 'votes' in lnk.attrs['href']][0]
    # TODO implement caching

    r = requests.get(csslink)

    css = r.content
    m = re.search('[.]starbar[ ]{width[:][ ](?P<width>[0-9]+)px',css)
    parent_width = float(m.groupdict()['width'])

    starbar_div = soup.select('div.starbar_w')
    child_width =  float(dict([i.split(':') for i in starbar_div[0].attrs['style'].split(';')])['width'].replace('px',''))

    print(parent_width,child_width)
    return round(child_width/parent_width *10,2)



def transform_data_dict(ddict):


    transforms= {

        #u'roд': lambda d: ('Films',{'freleasedate': datetime.datetime.strptime(d.text.strip(),"%Y%m%d")}),
        u'cтрана':lambda d:[('Countries', { 'name': c}) for c in commatlst(d)],
        u'жанр' : lambda d:[('Genres', { 'name':c }) for c in commatlst(d)],
        u'режиссер' : lambda d:[('Persons', {'name':c, 'p_type': APP_PERSON_DIRECTOR}) for c in commatlst(d)],
        u'продюсер' : lambda d:[('Persons', {'name':c, 'p_type': APP_PERSON_PRODUCER}) for c in commatlst(d)],
        u'бюджет': lambda d: [('Films',{'fbudget':int(''.join(d.text.replace(u'$','').split()))})],
        u'премьера (мир)': lambda d: [('Films',{'frelease_date': date_extract(d)})],
        u'премьера (РФ)' : lambda d: [('Films',{'frelease_date': date_extract(d)})],
        u'возраст': lambda d: [('Films',{'age_limit': int(
            [e for e in d.parent.select('div.ageLimit')[0].attrs['class']
            if not  e.endswith(u'Limit')][0].split('age')[-1])
                                     }
                            )],
        u'время' : lambda d :[('Films', {'fduration': int( d.parent.select('td.time')[0].text.split(u'мин.')[0]) })]
}
    tkeys = transforms.keys()
    for key,val in ddict.items():
        if key in tkeys:
            for el in transforms[key](val):
                yield el
        else:
            pass
            #print(u"Can't find parser for {}".format(key))

def get_photo(actor_id):

    try:
        r = requests.get(YANDEX_KP_ACTORS_TEMPLATE.format(actor_id))

        fileobj = StringIO.StringIO()
        fileobj.write(r.content)
        fileobj.seek(0)

        img = Image.open(fileobj).conver('RGB')

        conv_file = StringIO.StringIO()
        img.save(conv_file)
        conv_file.seek(0)

        return conv_file

    except:

        return None


def actors_wrap(actors_names):
   return [('Persons',{'name': an ,'p_type': APP_PERSON_ACTOR,
                       'photo': get_photo(re.match('[/]name[/](?P<id>[0-9]+)[/]',ai).groupdict()['id'])

                   }) for an,ai in actors_names]



def parse_one_page(page_id):

    parsed_data = []

    res = requests.get("http://www.kinopoisk.ru/film/%d/" % page_id, headers = headers)
    soup = BeautifulSoup(res.content.decode('cp1251'))

    info_table = soup.select("div#infoTable")[0]

    tds = info_table.select("td.type")
    data_dict = dict([(f.text,s) for f,s in [ td.parent.select("td") for td in tds]])
    parsed_data.extend(transform_data_dict(data_dict))


    actor_list = soup.select("div#actorList")[0]
    actors_n_l = [ (a.text,a.attrs['href']) for a in actor_list.find_all('a') if  not 'film' in a.attrs['href']]

    parsed_data.extend(actors_wrap(actors_n_l))

    brand_words = ('Films', {'description': soup.select("div.brand_words")[0].text})
    nametag=soup.select('h1.moviename-big')[0]
    moviename = ('Films', {'name':nametag.text})
    orig_movie_name = ('Films', {'name_orig':nametag.select('span')[0].text if len(nametag.select('span')) else ''})

    vote = ('Films',{'rating_kinopoisk': get_vote(soup)})

    parsed_data.extend([brand_words,moviename,orig_movie_name,vote])

    ddict = defaultdict(list)

    for pd in parsed_data:
        element,value = pd
        ddict[element].append(value)
    return ddict


if __name__ == "__main__":
    d = parse_one_page(41520)
    for di in d['Films']:

        for k in di :
            print(k)
            print(di[k])


