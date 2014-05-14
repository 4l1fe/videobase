from apps.films.models import Persons
from apps.robots.models import Robots
from crawler.parse_page import get_photo
from django.core.files import File



def get_person_poster(person_id):
    try:
        p = Persons.objects.get(id=person_id)
        if p.photo == '' and p.kinopoisk_id != None:
            p.photo.save('profile.jpg', File(get_photo(p.kinopoisk_id)))
    except Robots.DoesNotExist:
        pass
get_person_poster(1)