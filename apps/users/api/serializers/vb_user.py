# coding: utf-8
from rest_framework import serializers

from apps.users.models import User, UsersPics


class vbUser(serializers.HyperlinkedModelSerializer):
    avatar = serializers.SerializerMethodField('path_to_avatar')
    # extend
    # regdate
    # friends_cnt
    # films_watched
    # comments_cnt
    # genre_fav
    # relation

    # genres
    # genres

    # friends
    # friends

    def __init__(self, *args, **kwargs):
        super(vbUser, self).__init__(*args, **kwargs)

    def path_to_avatar(self, obj):
        userpic = obj.profile.userpic_id
        image = UsersPics.objects.get(id=userpic).image
        path = image.storage.url(image.name)
        return path

    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')
