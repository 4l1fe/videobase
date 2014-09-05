# coding: utf-8
from rest_framework import serializers
from apps.films.models import FilmExtras, Persons, PersonsFilms
from apps.users.models.users_feed import Feed
from .vb_user import vbUser
from django.core.cache import cache
from apps.users.constants import CACHED_FEED_TIMEOUT
from apps.users.constants import (FILM_RATE, FILM_SUBSCRIBE, FILM_NOTWATCH,
                                  FILM_COMMENT, FILM_O, PERSON_SUBSCRIBE,
                                  PERSON_O, USER_ASK, USER_FRIENDSHIP, SYS_ALL)


class vbFeedElement(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_vbUser')
    object = serializers.SerializerMethodField('get_object')

    def __init__(self, *args, **kwargs):
        super(vbFeedElement, self).__init__(*args, **kwargs)
        self.films = ''
        self.persons = ''
        self.users_films = ''
        self.comments = ''
        self.persons_films = ''

    def get_object(self,obj):
        key = '{},{},{}'.format(obj.user.id, obj.type, obj.obj_id)
        object_ = cache.get(key)
        if not object_:
            if obj.type == FILM_RATE:
                film = self.films.get(pk=obj.obj_id)
                rating = self.users_films.get(film=film).rating
                object_ = {'id': film.id,
                          'name': film.name,
                          'rating': rating}
            elif obj.type == FILM_SUBSCRIBE:
                film = self.films.get(pk=obj.obj_id)
                poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
                object_ = {'id': film.id,
                          'name': film.name,
                          'poster': poster,
                          'description': film.description}
            elif obj.type == FILM_NOTWATCH:
                film = self.films.get(pk=obj.obj_id)
                object_ = {'id': film.id,
                          'name': film.name}
            elif obj.type == FILM_COMMENT:
                comment = self.comments.get(pk=obj.obj_id)
                film = comment.content.film
                object_ = {'id': comment.id,
                           'text': comment.text,
                           'film': {'id': film.id,
                                    'name': film.name}}
            elif obj.obj_id == FILM_O:
                film = self.films.get(pk=obj.obj_id)
                poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
                object_ = {'id': film.id,
                           'name': film.name,
                           'poster': poster,
                           'locations': []}  # TODO: доделать
            elif obj.type == PERSON_SUBSCRIBE:
                person = self.persons.get(obj.obj_id)
                object_ = {'id': person.id,
                           'name': person.name,
                           'photo': person.get_path_to_photo}
            elif obj.type == PERSON_O:
                person = self.persons.get(obj.obj_id)
                p_type = self.persons_films.get(person=person).p_type
                film = ''  # TODO: не определить, надо сохранять его в Feed при событии
                object_ = {'id': person.id,
                           'name': person.name,
                           'photo': person.get_path_to_photo,
                           'type': p_type,
                           'film': {'id': '',
                                    'name': ''}}
            elif obj.type == USER_ASK:


            cache.set(key, object_, CACHED_FEED_TIMEOUT)

        return object_
    
    def get_vbUser(self, obj):
        return vbUser(obj.user).data

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')
