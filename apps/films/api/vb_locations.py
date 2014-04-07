# coding: utf-8

from rest_framework import serializers

from apps.films.models import Films

from apps.contents.models import Contents, Locations


class vbLocationsFilmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Films
        fields = ['id', 'name', 'name_orig',\
                  # 'release_date', 'poster', \
                  # 'relation', 'ratings', 'duration', 'locations', 'countries',
                  # 'description', \
                 ]
