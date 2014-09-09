# coding: utf-8
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.contents.models import Locations
from apps.users.models import Feed
from apps.users.constants import FILM_O, PERSON_O
from apps.films.models import Persons

__all__ = ['post_save_handler']


@receiver(post_save, sender=Locations)
def post_save_handler(sender, **kwargs):
    if kwargs['created']:
        if sender.objects.filter(content=kwargs['instance'].content).count() == 1:
            location = kwargs['instance']

            # Событие появление подписки на фильм
            film = location.content.film
            Feed.objects.create(type=FILM_O, obj_id=film.id, child_obj_id=location.id)

            # Событие появление подписки на персону
            persons = Persons.objects.filter(pf_persons_rel__film=film.id).\
                extra(select={'p_type': "persons_films.p_type"})

            for person in persons:
                Feed.objects.create(type=PERSON_O, obj_id=person.id, child_obj_id=film.id)