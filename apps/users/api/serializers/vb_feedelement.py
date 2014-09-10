# coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from apps.contents.models import Comments, Locations
from apps.films.models import FilmExtras, Persons, PersonsFilms, Films, UsersFilms
from apps.users import UsersPics
from apps.users.models.users_feed import Feed
from apps.users.api.serializers import vbUser
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
        self.user_data = {}  # собираем заранее данные по различным пользователям
        for ins in self.object:
            if ins.user_id and ins.user_id not in self.user_data:
                self.user_data.update({ins.user_id: vbUser(ins.user).data})

    def get_object(self, obj):
        user_id = obj.user_id if obj.user_id else ''  # может придти None. Не во всех событиях указывается пользователь
        key = '{},{},{}'.format(user_id, obj.type, obj.obj_id)
        object_ = cache.get(key)
        if not object_:
            try:
                if obj.type == FILM_RATE:
                    film = Films.objects.get(pk=obj.obj_id)
                    rating = UsersFilms.objects.get(user_id=obj.user_id, film=film).rating
                    object_ = {'id': film.id,
                              'name': film.name,
                              'rating': rating}
                elif obj.type == FILM_SUBSCRIBE:
                    film = Films.objects.get(pk=obj.obj_id)
                    poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
                    object_ = {'id': film.id,
                              'name': film.name,
                              'poster': poster,
                              'description': film.description}
                elif obj.type == FILM_NOTWATCH:
                    film = Films.objects.get(pk=obj.obj_id)
                    poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
                    object_ = {'id': film.id,
                              'name': film.name,
                              'poster': poster}
                elif obj.type == FILM_COMMENT:
                    comment = Comments.objects.get(pk=obj.obj_id)
                    film = Films.objects.get(pk=obj.child_obj_id)
                    object_ = {'id': comment.id,
                               'text': comment.text,
                               'film': {'id': film.id,
                                        'name': film.name}}
                elif obj.obj_id == FILM_O:
                    film = Films.objects.get(pk=obj.obj_id)
                    poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
                    location = Locations.objects.get(pk=obj.child_obj_id)
                    object_ = {'id': film.id,
                               'name': film.name,
                               'poster': poster,
                               'location': {'id': location.id,  # TODO: сделать массивом
                                            'name': location.name,
                                            'price': location.price,
                                            'price_type': location.price_type}}
                elif obj.type == PERSON_SUBSCRIBE:
                    person = Persons.objects.get(pk=obj.obj_id)
                    object_ = {'id': person.id,
                               'name': person.name,
                               'photo': person.get_path_to_photo}
                elif obj.type == PERSON_O:
                    person = Persons.objects.get(pk=obj.obj_id)
                    film = Films.objects.get(pk=obj.child_obj_id)
                    pf = PersonsFilms.objects.filter(person=person, film=film).first()  #TODO: брать роль по статистике
                    object_ = {'id': person.id,
                               'name': person.name,
                               'photo': person.get_path_to_photo,
                               'type': pf.p_type,
                               'film': {'id': film.id,
                                        'name': film.name}}
                elif obj.type == USER_ASK:
                    friend = User.objects.get(pk=obj.obj_id)
                    try:
                        a = UsersPics.objects.get(user=friend).image
                        avatar = a.storage.url(a.name)
                    except:
                        avatar = ''
                    object_ = {'id': friend.id,
                               'name': friend.username,
                               'avatar': avatar}
                elif obj.type == USER_FRIENDSHIP:
                    friend = User.objects.get(pk=obj.obj_id)
                    try:
                        a = UsersPics.objects.get(user=friend).image
                        avatar = a.storage.url(a.name)
                    except:
                        avatar = ''
                    object_ = {'id': friend.id,
                               'name': friend.username,
                               'avatar': avatar}
                elif obj.type == SYS_ALL:
                    object_ = {}
            except Exception as e:
                object_ = {}

            cache.set(key, object_, CACHED_FEED_TIMEOUT)

        return object_

    def get_vbUser(self, obj):
        return self.user_data.get(obj.user_id, {})

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')