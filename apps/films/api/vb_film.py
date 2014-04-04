# coding: utf-8

from rest_framework import serializers
import rest_framework.fields

from apps.films.models import Films, FilmExtras, Countries, Genres, PersonsFilms, Persons
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER

from apps.contents.models import Contents, Locations


#############################################################################################################
#
class CountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id', 'name')


#############################################################################################################
#
class GentriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'name')


#############################################################################################################
#
class PersonsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        new_fields = []
        extend = kwargs.pop('extend', False)

        if not extend:
            new_fields += ['bio']

        # Instantiate the superclass normally
        super(PersonsSerializer, self).__init__(*args, **kwargs)

        if len(new_fields):
            # Drop keys if they exist
            for field_name in new_fields:
                self.fields.pop(field_name, None)


    class Meta:
        model = Persons
        fields = ('id', 'name', 'photo', 'bio')


#############################################################################################################
#
class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        exclude = ('content',)


#############################################################################################################
#
class vbFilmSerializer(serializers.HyperlinkedModelSerializer):
    locations = LocationsSerializer()
    countries = CountriesSerializer()
    genres = GentriesSerializer()
    persons = PersonsSerializer()
    ratings = serializers.SerializerMethodField('calc_ratings')

    def __init__(self, *args, **kwargs):
        new_fields = []
        extend = kwargs.pop('extend', False)

        if not extend:
            new_fields += ['description', 'genres', 'countries']

        persons = kwargs.pop('persons', False)
        if not persons:
            new_fields += ['persons']

        # Instantiate the superclass normally
        super(vbFilmSerializer, self).__init__(*args, **kwargs)

        if len(new_fields):
            # Drop keys if they exist
            for field_name in new_fields:
                self.fields.pop(field_name, None)


    def calc_ratings(self, obj):
        return {
            'imdb': [obj.rating_imdb, obj.rating_imdb_cnt],
            'kp': [obj.rating_kinopoisk, obj.rating_kinopoisk_cnt],
            'cons': [0, 0],
        }


    class Meta:
        model = Films
        fields = ['id', 'name', 'name_orig', 'release_date', \
                  'ratings', 'duration', #'locations', 'relation', 'poster',
                  'description', 'countries', 'genres', 'persons',
                 ]
    #
    # def to_native(self, obj):
    #     del self.fields['name']
    #     return obj

    def work(self):
        pass
