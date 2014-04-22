# coding: utf-8

from rest_framework import serializers

from apps.films.api.serializers import vbUserGenre
from apps.films.models import Genres

from apps.users.models import User, UsersPics, UsersRels
from apps.users.constants import APP_USER_REL_TYPE_NONE, APP_USER_REL_TYPE_FRIENDS


class vbUser(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('path_to_avatar')

    # extend
    regdate = serializers.SerializerMethodField('get_regdate')
    friends_cnt = serializers.SerializerMethodField('get_friends_cnt')
    films_watched = serializers.SerializerMethodField('get_films_watched_cnt')
    comments_cnt = serializers.SerializerMethodField('get_comments_cnt')

    # genre_fav
    relation = serializers.SerializerMethodField('get_relation')

    # genres
    genres = serializers.SerializerMethodField('genres_list')

    # friends
    friends = serializers.SerializerMethodField('friends_list')

    def __init__(self, *args, **kwargs):
        self.cer_user = kwargs.pop('cer_usre', None)
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

    def path_to_avatar(self, obj):
        userpic = obj.profile.userpic_id
        try:
            image = UsersPics.objects.get(id=userpic).image
            path = image.storage.url(image.name)
        except:
            path = ''
        return path

    def get_regdate(self, obj):
        return obj.date_joined

    def get_friends_cnt(self, obj):
        return UsersRels.objects.filter(user=obj, rel_type=APP_USER_REL_TYPE_FRIENDS).count()

    def get_films_watched_cnt(self, obj):
        return 0

    def get_comments_cnt(self, obj):
        return obj.comments.all().count()

    def get_relation(self, obj):
        try:
            rel = UsersRels.objects.get(user=obj, user_rel=self.cer_user).rel_type
        except:
            rel = APP_USER_REL_TYPE_NONE
        return rel

    def genres_list(self, obj):
        genres = Genres.objects.filter(genres__users_films__user=obj)
        serializer = vbUserGenre(genres, many=True)
        return serializer.data

    def friends_list(self, obj):
        friends = UsersRels.objects.filter(user=obj, rel_type=APP_USER_REL_TYPE_FRIENDS)
        serializer = vbUser(friends, cer_usre=self.cer_user, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'regdate',
                  'friends_cnt', 'films_watched', 'comments_cnt',
                  'relation', 'genres', 'friends')
