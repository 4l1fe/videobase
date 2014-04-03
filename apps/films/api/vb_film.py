# coding: utf-8

from rest_framework import serializers

from apps.films.models import Films, FilmExtras, Countries
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER

from apps.contents.models import Contents, Locations



class CountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id', 'name')


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations





class vbFilmSerializer(serializers.ModelSerializer):
    # locations = LocationsSerializer()
    # countries = CountriesSerializer()

    class Meta:
        model = Films
        fields = ['id', 'name', 'name_orig',\
                  # 'release_date', 'poster', \
                  # 'relation', 'ratings', 'duration', 'locations', 'countries',
                  # 'description', \
                 ]

    def work(self):
        pass
