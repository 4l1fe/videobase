# coding: utf-8

from rest_framework import serializers

from apps.films.models import *
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER
from apps.contents.models import *

from utils.common import group_by, reindex_by, list_of
from utils.middlewares.local_thread import get_current_request

from vb_person import vbPerson


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
class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations


#############################################################################################################
#
class ContentSerializer(serializers.ModelSerializer):
    film = LocationsSerializer()

    class Meta:
        model = Locations
        fields = ('id', 'film',)


#############################################################################################################
#
class vbFilm(serializers.HyperlinkedModelSerializer):
    countries = CountriesSerializer()
    genres = GentriesSerializer()
    persons = vbPerson()
    ratings = serializers.SerializerMethodField('calc_ratings')
    locations = serializers.SerializerMethodField('locations_list')
    poster = serializers.SerializerMethodField('poster_list')
    relation = serializers.SerializerMethodField('relation_list')

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

    def locations_list(self, obj):
        # Select contents by films
        contents = Contents.objects.filter(film__in=[obj.pk]).values('id', 'film')
        # result = LocationsSerializer(contents)
        contents_list = list_of(contents, 'id', False, True)

        # Select locations contents by contents
        locations = Locations.objects.filter(content__in=contents_list)
        locations = reindex_by(locations, 'content_id', True)

        # Rebuild data
        result = {}
        for item in contents:
            ser = LocationsSerializer(locations[item['id']])
            result[item['film']] = ser.data

        return result.get(obj.pk, [])

    def poster_list(self, obj):
        extras = FilmExtras.objects.filter(film__in=[obj.pk], etype=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)
        extras = group_by(extras, 'id', True)

        return [item.url for item in extras.get(obj.pk, []) if len(item.url)]

    def relation_list(self, obj):
        req = get_current_request()
        if req.user.is_authenticated():
            pass

        return []

    class Meta:
        model = Films
        fields = ['id', 'name', 'name_orig', 'release_date', \
                  'ratings', 'duration', 'locations', 'poster', 'relation', \
                  'description', 'countries', 'genres', 'persons',
                 ]
