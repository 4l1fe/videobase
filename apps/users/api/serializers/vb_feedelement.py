# coding: utf-8

from rest_framework import serializers
from apps.users.models.users_feed import Feed
from .vb_user import vbUser


class vbFeedElement(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_vbUser')
    object = serializers.SerializerMethodField('get_Object')

    def get_Object(self,obj):
        return obj.object
    
    def get_vbUser(self, obj):
        return vbUser(obj.user).data

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')
