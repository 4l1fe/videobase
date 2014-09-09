# coding: utf-8

from rest_framework import serializers

from apps.casts.models import Casts, UsersCasts
from apps.users.api.serializers import vbUser

class vbCastChatMsg(serializers.ModelSerializer):

    user = serializers.SerializerMethodField('calc_user')

    def calc_user(self, obj):
        return vbUser(obj.user)

    class Meta:
        model = Casts
        fields = (
            'id', 'cast_id', 'created', 'text'
        )



