# coding: utf-8
from rest_framework import serializers

from apps.films.models import Genres


class vbUserGenre(serializers.ModelSerializer):
    procent = serializers.SerializerMethodField('calc_procent')

    def calc_procent(self, obj):
        return 0

    class Meta:
        model = Genres
        fields = ('id', 'name', 'procent')
