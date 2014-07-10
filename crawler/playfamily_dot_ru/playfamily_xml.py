
from apps.films.models import Films
from bs4 import BeautifulSoup

from crawler.tor import get_page_or_renew
from crawler.tor import simple_tor_get_page
from crawler.utils.locations_utils import sane_dict,save_location
from crawler.kinopoisk_ru.kinopoisk import get_genre, get_country
from crawler.task_modules.kinopoisk_one_page import kinopoisk_parse_one_film
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_PAY
from django.utils import timezone

PLAYFAMILY_XML= 'http://playlite.ru/widgets/partner/catalog/p661.xml'


def get_soup():
    '''
    Getting data from playfamily site and parsing its xml into BeautfulSoup object
    
    '''
    xmldata = simple_tor_get_page(PLAYFAMILY_XML)
    soup = BeautifulSoup(xmldata,'xml')
    return soup

def extract_info(soup):
    '''
    Accepting @soup object,

    Returns dict with data extracted from this soup.

    Particulary following keys expected,

    genres,countries,title,originalFileName,duration,kinopoiskId,price
    '''

    for fe in soup.find_all('catalogElement'):

        gts = fe.find('genres')
        if gts:
            gs = [gtag.text for gtag in gts]
            gts.extract()
        else:
            gs = []
        cts = fe.find('countries')
        if cts:
            cs = [ctag.text for ctag in cts]
            cts.extract()
        else:
            cs = []
        d = dict( (e.name,e.text) for e in fe)

        d.update({'genres':gs,'countries':cs})

        yield d

def extract_url(tag):
    iframe_soup = BeautifulSoup(tag)
    return iframe_soup.find('iframe').attrs['src']
    
        
def process(soup = None):
    '''
    Update our database using information from freshly downloaded xml from playfamily.ru

    Can accept non mandatory parameter @soup. If there is no soup supplied function downloads
    new one from url set in PLAYFAMILY_XML constant
    '''
    
    if soup is None:
        soup = get_soup()

    info_iter = [e for e in extract_info(soup)]
    for info in info_iter:
        kinopoisk_id = info['kinopoiskId'] if type(info['kinopoiskId']) is int else int(info['kinopoiskId'])
        try:
            film = Films.objects.get(kinopoisk_id=kinopoisk_id)
            print "Found {} in our database".format(film)

            if not film.name.strip():
                film.name = info['title']
                film.save()
            if not film.name_orig.strip():
                film.name_orig = info['originalFilename']
                film.save()

            if not film.duration:
                film.duration = int(info['duration'])
        except Films.DoesNotExist:
            print u"Couldn't found film {} in our database trying to create one".format(info['title'])
            film = Films(name=info['title'],
                        name_orig=info['originalFilename'],
                        description=0,
                        duration=int(info['duration']),
                        release_date=timezone.datetime.strptime(info['releaseYear'], "%Y"),
                        kinopoisk_id=kinopoisk_id
            )
            film.save()
            print "Succesfully created {}. Trying to schedule update".format(film)
            kinopoisk_parse_one_film.apply_async(
            (
                 kinopoisk_id,
                info['title']
                 )
            )
            print "Update scheduled"

        data_dict = sane_dict(film)

        data_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_PAY
        data_dict['price'] = int(float(info['price']))
        data_dict['type'] = 'playfamily'
        data_dict['value'] = info['uid']
        data_dict['url_view'] = extract_url(info['frame'])
        save_location(**data_dict)


#film = Films.objects.get(kinopoisk_id=d['kinopoiskId'])

