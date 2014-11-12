# coding: utf-8

from rest_framework import serializers

from apps.casts.models import CastsChatsMsgs
from apps.users.api.serializers import vbUser


class vbCastChatMsg(serializers.ModelSerializer):

    cast_id = serializers.IntegerField(source='cast.id')
    user = vbUser()

    class Meta:
        model = CastsChatsMsgs
        fields = ('id', 'created', 'text', 'cast_id', 'user')



