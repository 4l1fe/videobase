# coding: utf-8

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contents.models import Locations
from apps.users.models import Feed
from apps.users.constants import FILM_O, PERSON_O

__all__ = ['post_save_handler']

@receiver(post_save, sender=Locations)
def post_save_handler(sender, **kwargs):
    if kwargs['created']:
        if sender.objects.filter(content=kwargs['instance'].content).count() == 1:
            location = kwargs['instance']
            film = location.content.film
            obj = {'id': film.id, 'name': film.name, 'poster': u'', 'location': {'id': location.id,\
                                                                                 'name': location.type, 'price': location.price, 'price_type': location.price_type}}
            Feed.objects.create(type=FILM_O, object=obj)

            persons = film.persons.all()
            for person in persons:
                pers_obj = {'id': person.id, 'name': person.name, 'photo': u'', 'type': '', 'film': {'id': film.id, 'name': film.name}}
                Feed.objects.create(type=PERSON_O, object=pers_obj)
