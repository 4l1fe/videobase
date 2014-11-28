# coding: utf-8
from rest_framework import serializers
from apps.casts.models import CastExtrasStorage


################################################################################
class vbExtra(serializers.ModelSerializer):

    class Meta:
        model = CastExtrasStorage
        fields = ('id', 'name')