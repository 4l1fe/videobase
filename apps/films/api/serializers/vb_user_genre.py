# coding: utf-8
from rest_framework import serializers

from apps.films.models import Genres


class vbUserGenre(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField('calc_percent')

    def calc_percent(self, obj):
        return 0

    class Meta:
        model = Genres
        fields = ('id', 'name', 'percent')
