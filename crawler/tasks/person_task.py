
from bs4 import BeautifulSoup

from django.core.files import File

from apps.films.models import Persons

from crawler.datarobots.kinopoisk_ru.parse_page import get_photo
from crawler.tasks.utils import robot_task
from crawler.tor import simple_tor_get_page

from utils.common import traceback_own


__author__ = 'vladimir'

@robot_task('kinopoisk_persons')
def parse_kinopoisk_persons(pid):
    update_kinopoisk_persone(pid)


def update_kinopoisk_persone(pid):
    try:
        response = simple_tor_get_page('http://www.kinopoisk.ru/name/{}/view_info/ok/#trivia'.format(pid), True)

        soup = BeautifulSoup(response)
        tag = soup.find('span', attrs={'itemprop': 'alternativeHeadline'})
        orig_name = tag.text.strip()

        p = Persons.objects.get(kinopoisk_id=pid)
        tag_birthdate = soup.find('td', attrs={'class': 'birth'})

        birthdate = ''
        print "ID = ", p.id
        if not (tag_birthdate is None):
            birthdate = tag_birthdate.get('birthdate')
        else:
            print 'No data birthdate for this person id = {}'.format(pid)

        bio = ''
        tags_bio = soup.findAll('li', attrs={'class': 'trivia'})
        if len(tags_bio):
            for li in tags_bio:
                bio = bio + ' ' + li.text
        else:
            print 'No biography for this person id = {}'.format(pid)

        p.bio = bio
        p.kinopoisk_id = pid
        p.name_orig = orig_name
        p.birthdate = birthdate

        if p.photo == '' and p.kinopoisk_id != 0:
            p.photo.save('profile.jpg', File(get_photo(p.kinopoisk_id)))

        p.save()
    except Exception, e:
        traceback_own(e)
