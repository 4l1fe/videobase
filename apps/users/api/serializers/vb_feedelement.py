# coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from apps.contents.models import Comments, Locations
from apps.films.models import FilmExtras, PersonsFilms, Films, UsersFilms
from apps.users import UsersPics
from apps.users.models.users_feed import Feed
from apps.users.api.serializers import vbUser
from apps.users.constants import (FILM_RATE, FILM_SUBSCRIBE, FILM_NOTWATCH,
                                  FILM_COMMENT, FILM_O, PERSON_SUBSCRIBE,
                                  PERSON_O, USER_ASK, USER_FRIENDSHIP, SYS_ALL)
from django.db.models.query import QuerySet
from utils.common import isiterable


class vbFeedElement(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_field')
    object = serializers.SerializerMethodField('get_object_field')

    def __init__(self, *args,  **kwargs):
        super(vbFeedElement, self).__init__(*args, **kwargs)
        self.feeds = self.object

        if not (isinstance(self.feeds, QuerySet) or isinstance(self.feeds, Feed)):
            raise TypeError('object must be QuerySet or Feed instance')
        
        if not isiterable(self.feeds):
            self.feeds = [self.feeds]

        # собираем заранее данные по различным пользователям
        self.user_data = {}
        for f in self.feeds:
            if f.user_id and f.user_id not in self.user_data:
                self.user_data.update({f.user_id: vbUser(f.user).data})

        # собираем инфу по фильмам
        self.films = {}
        films_id = self._get_only_films_id()
        for film in Films.objects.filter(pk__in=films_id):
            poster = FilmExtras.get_poster_by_film(film.fe_film_rel.all())
            self.films[film.id] = {
                'name': film.name,
                'description': film.description,
                'poster': poster
            }

        # собираем инфу по рейтингам
        users_films = UsersFilms.objects.\
            filter(user_id__in=self.user_data.keys(), film_id__in=films_id).\
            values('user_id', 'film_id', 'rating')

        self.ratings = {(uf['user_id'], uf['film_id']): uf['rating'] for uf in users_films}

        # собираем инфу по персонам
        self.persons = {}
        persons_id = [f.obj_id for f in self.feeds if f.type in (PERSON_SUBSCRIBE, PERSON_O)]
        for pf in PersonsFilms.objects.filter(person_id__in=persons_id).select_related():
            if pf.person.id not in self.persons:
                # TODO: брать роль по статистике
                self.persons[pf.person.id] = {
                    'name': pf.person.name,
                    'photo': pf.person.get_path_to_photo,
                    'type': pf.p_type
                }

    def _get_only_films_id(self):
        # собираем из пришедших событий только id фильмов
        films_id = []
        for feed in self.feeds:
            if feed.type in [FILM_RATE, FILM_SUBSCRIBE, FILM_NOTWATCH, FILM_O]:
                films_id.append(feed.obj_id)
            if feed.type in [FILM_COMMENT, PERSON_O]:
                films_id.append(feed.child_obj_id)

        return films_id

    #формирование полей в отдаче
    def get_object_field(self, obj):
        """
        Оборачиваем везде исключениями,
        чтобы заглушалось только какое-то конкретное событие, но не все.
        Не везде сделаны предвыборки, предполагается, что некоторые типы событий в ленту будут попадать не часто...
        """

        feed = obj
        object_ = {}
        if feed.type == FILM_RATE:
            try:
                rating = self.ratings[(feed.user_id, feed.obj_id)]
                object_ = {
                    'id': feed.obj_id,
                    'name': self.films[feed.obj_id]['name'],
                    'rating': rating
                }
            except Exception, e:
                object_ = {}

        elif feed.type == FILM_SUBSCRIBE:
            try:
                object_ = {
                    'id': feed.obj_id,
                    'name': self.films[feed.obj_id]['name'],
                    'poster': self.films[feed.obj_id]['poster'],
                    'description': self.films[feed.obj_id]['description']
                }
            except Exception, e:
                object_ = {}

        elif feed.type == FILM_NOTWATCH:
            try:
                object_ = {
                    'id': feed.obj_id,
                    'name': self.films[feed.obj_id]['name'],
                    'poster': self.films[feed.obj_id]['poster']
                }
            except Exception, e:
                object_ = {}

        elif feed.type == FILM_COMMENT:
            try:
                comment = Comments.objects.get(pk=feed.obj_id)
                object_ = {
                    'id': comment.id,
                    'text': comment.text,
                    'film': {
                        'id': feed.child_obj_id,
                        'name': self.films[feed.child_obj_id]['name']
                    }
                }
            except Exception, e:
                object_ = {}

        elif feed.obj_id == FILM_O:
            try:
                location = Locations.objects.get(pk=feed.child_obj_id)
                object_ = {
                    'id': feed.obj_id,
                    'name': self.films[feed.obj_id]['name'],
                    'poster': self.films[feed.obj_id]['poster'],
                    'locations': [{
                        'id': location.id,  # TODO: сделать массивом
                        'name': location.name,
                        'price': location.price,
                        'price_type': location.price_type
                    }]
                }
            except Exception, e:
                object_ = {}

        elif feed.type == PERSON_SUBSCRIBE:
            try:
                object_ = {
                    'id': feed.obj_id,
                    'name': self.persons[feed.obj_id]['name'],
                    'photo': self.persons[feed.obj_id]['photo']
                }
            except Exception, e:
                object_ = {}

        elif feed.type == PERSON_O:
            try:
                object_ = {
                    'id': feed.obj_id,
                    'name': self.persons[feed.obj_id]['name'],
                    'photo': self.persons[feed.obj_id]['photo'],
                    'type': self.persons[feed.obj_id]['type'],
                    'film': {
                        'id': feed.child_obj_id,
                        'name': self.films[feed.child_obj_id]['name']
                    }
                }
            except Exception, e:
                object_ = {}

        elif feed.type == USER_ASK:
            try:
                friend = User.objects.get(pk=feed.obj_id)
                object_ = {
                    'id': friend.id,
                    'name': friend.username
                }

                try:
                    a = UsersPics.objects.get(user=friend).image
                    avatar = a.storage.url(a.name)
                    object_.update({'avatar': avatar})
                except:
                    object_.update({'avatar': ''})
            except Exception, e:
                object_ = {}

        elif feed.type == USER_FRIENDSHIP:
            try:
                friend = User.objects.get(pk=feed.obj_id)
                object_ = {
                    'id': friend.id,
                    'name': friend.username
                }

                try:
                    a = UsersPics.objects.get(user=friend).image
                    avatar = a.storage.url(a.name)
                    object_.update({'avatar': avatar})
                except:
                    object_.update({'avatar': ''})
            except Exception, e:
                object_ = {}

        elif feed.type == SYS_ALL:
            object_ = {}

        return object_

    def get_user_field(self, obj):
        return self.user_data.get(obj.user_id, {})

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')
