# coding: utf-8

from rest_framework import serializers

from apps.casts.models import Casts, UsersCasts, CastsChatsMsgs
from apps.users.api.serializers import vbUser

class vbCastChatMsg(serializers.ModelSerializer):

    user = serializers.SerializerMethodField('calc_user')
    cast_id = serializers.SerializerMethodField('calc_cast_id')

    def calc_cast_id(self, obj):

        return obj.cast.id

    def calc_user(self, obj):
        return vbUser(obj.user)

    
    class Meta:
        model = CastsChatsMsgs
        fields = (
            'id', 'created', 'text'
        )



