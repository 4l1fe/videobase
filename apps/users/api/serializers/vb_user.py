# coding: utf-8
from django.db.models import Count
from django.db.models import Q

from rest_framework import serializers

from apps.films.api.serializers import vbUserGenre
from apps.films.models import Genres, UsersFilms, Films
from apps.films.constants import APP_USERFILM_STATUS_NOT_WATCH, APP_USERFILM_STATUS_UNDEF, APP_USERFILM_STATUS_PLAYLIST

from apps.users.models import User, UsersPics, UsersRels
from apps.users.constants import APP_USER_REL_TYPE_NONE, APP_USER_REL_TYPE_FRIENDS

#:TODO Нужно отрефакторить vbUser. Волосы дыбом стоия когда его читаешь.
#:TODO Необходимо сделать замеры количества запросов, есть подозрение что можно сэкономить


class vbUser(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    avatar = serializers.SerializerMethodField('path_to_avatar')

    # Признак extend
    regdate = serializers.SerializerMethodField('get_regdate')
    friends_cnt = serializers.SerializerMethodField('get_friends_cnt')
    films_watched = serializers.SerializerMethodField('get_films_watched_cnt')
    comments_cnt = serializers.SerializerMethodField('get_comments_cnt')
    genre_fav = serializers.SerializerMethodField('get_genre_fav')
    relation = serializers.SerializerMethodField('get_relation')

    # Признак genres
    genres = serializers.SerializerMethodField('genres_list')

    # Признак friends
    friends = serializers.SerializerMethodField('friends_list')

    def __init__(self, *args, **kwargs):
        self.cer_user = kwargs.pop('cer_user', None)
        del_fields = []
        extend = kwargs.pop('extend', False)
        if not extend:
            del_fields += ['regdate', 'friends_cnt', 'films_watched',
                           'comments_cnt', 'relation']

        genres = kwargs.pop('genres', False)
        if not genres:
            del_fields += ['genres']

        friends = kwargs.pop('friends', False)
        if not friends:
            del_fields += ['friends']

        super(vbUser, self).__init__(*args, **kwargs)

        if del_fields:
            # Drop keys if they exist
            for field_name in del_fields:
                self.fields.pop(field_name, None)

    def get_name(self, obj):
        return obj.profile.get_name()

    def get_genre_fav(self, obj):  # TODO: пока что алгоритма для любимого жанра нету, берём первый из любимых.
        genre_list = self.genres_list(obj)
        if genre_list:
            return genre_list[0]

        return []

        # try:
        #     genre = Genres.objects.filter(genres__uf_films_rel__user=obj).\
        #         exclude(genres__uf_films_rel__status=APP_USERFILM_STATUS_NOT_WATCH).distinct().values("id", "name").\
        #         annotate(count=Count("genres__id"))
        #     genre = max(genre, key=lambda g: g['count'])
        # except Exception, e:
        #     return {}
        #
        # if 'id' in genre and 'name' in genre:
        #     return {'id': genre['id'], 'name': genre['name']}
        #
        # return {}

    def path_to_avatar(self, obj):
        return UsersPics.get_picture(obj.profile)

    def get_regdate(self, obj):
        return obj.date_joined

    def get_friends_cnt(self, obj):
        return UsersRels.objects.filter(user=obj, rel_type=APP_USER_REL_TYPE_FRIENDS).count()

    def get_films_watched_cnt(self, obj):
        return UsersFilms.objects.filter(user=obj, rating__gt=0).count()

    def get_comments_cnt(self, obj):
        return obj.comments.all().count()

    def get_relation(self, obj):
        rel = APP_USER_REL_TYPE_NONE
        try:
            rel = UsersRels.objects.get(user=obj, user_rel=self.cer_user).rel_type
        except Exception, e:
            pass

        return rel

    def genres_list(self, obj):
        user_films = list(Films.objects.filter(Q(uf_films_rel__user=obj), ~Q(uf_films_rel__status=APP_USERFILM_STATUS_NOT_WATCH)).values_list('pk', flat=True))
        genres = Genres.get_full_genres_by_films(user_films)
        return sorted(vbUserGenre(genres, user=obj, many=True).data, key=lambda g: g['percent'], reverse=True)

    def friends_list(self, obj):
        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, obj.pk]).all()

        return vbUser(friends, cer_user=self.cer_user, many=True).data

    class Meta:
        model = User
        fields = (
            'id', 'name', 'avatar', 'regdate',
            'friends_cnt', 'films_watched', 'comments_cnt',
            'relation', 'genres', 'friends', 'genre_fav'
        )
