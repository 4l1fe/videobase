# coding: utf-8

from rest_framework import serializers
from apps.users.models.users_feed import Feed
from .vb_user import vbUser


class vbFeedElement(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_vbUser')

    def get_vbUser(self, obj):
        return vbUser(obj.user)

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')
