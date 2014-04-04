# coding: utf-8

from rest_framework import serializers
from apps.films.models import FilmExtras


#############################################################################################################
#
class vbExtra(serializers.ModelSerializer):

    class Meta:
        model = FilmExtras
        fields = ('id', 'name', 'name_orig', 'type', 'description', 'url')
