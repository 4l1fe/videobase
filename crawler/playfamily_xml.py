
from apps.films.models import Films
from bs4 import BeautifulSoup

from tor import get_page_or_renew
from crawler.core.browser import get_random_weighted_browser_string
from crawler.locations_utils import sane_dict,save_location
from crawler.kinopoisk import get_genre, get_country
from crawler.task_modules.kinopoisk_one_page import kinopoisk_parse_one_film
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_PAY
from django.utils import timezone

PLAYFAMILY_XML= 'http://playlite.ru/widgets/partner/catalog/p661.xml'


def get_soup():
    xmldata = get_page_or_renew(PLAYFAMILY_XML, user_agent =get_random_weighted_browser_string())

    soup = BeautifulSoup(xmldata,'xml')

    return soup

def extract_info(soup):

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

    if soup is None:
        soup = get_soup()

    info_iier = extract_info(soup)

    for info in info_iier:

        try:
            film = Films.objects.get( kinopoisk_id= info['kinopoiskId'])
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
            film= Films(name = info['title'],
                        name_orig = info['originalFilename'],
                        description =0, duration = int(info['duration']),
                        release_date = timezone.datetime.strptime(info['releaseYear'],"%Y")
                                                   
            )
            film.save()
            print "Succesfully created {}. Trying to schedule update".format(film)
            kinopoisk_parse_one_film.apply_async(
                (info['title'],
                 info['kinopoiskId'])
            )
            print "Update scheduled"

            
                        
    d = sane_dict(film)

    d['price_type'] = APP_CONTENTS_PRICE_TYPE_PAY
    d['price']= int(info['price'])

    d['url_view'] = extract_url(d['frame'])
    save_location(**d)
    





    

#film = Films.objects.get(kinopoisk_id=d['kinopoiskId'])
