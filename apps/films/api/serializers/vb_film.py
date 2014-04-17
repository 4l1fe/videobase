# coding: utf-8

from django.core.paginator import Page

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

# class LocationsSerializer(serializers.Serializer):
#
#     class Meta:
#         model = Locations


#############################################################################################################
#
class ContentSerializer(serializers.ModelSerializer):
    film = LocationsSerializer()

    class Meta:
        model = Locations
        fields = ('id', 'film',)


#############################################################################################################
#
class vbFilm(serializers.ModelSerializer):
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
        super(vbFilm, self).__init__(*args, **kwargs)

        if len(new_fields):
            # Drop keys if they exist
            for field_name in new_fields:
                self.fields.pop(field_name, None)

        self._get_obj_list()
        self._rebuild_location()
        self._rebuild_poster_list()


    def calc_ratings(self, obj):
        return {
            'imdb': [obj.rating_imdb, obj.rating_imdb_cnt],
            'kp': [obj.rating_kinopoisk, obj.rating_kinopoisk_cnt],
            'cons': [0, 0],
        }


    def _get_obj_list(self):
        list_pk = []

        if hasattr(self.object, '__iter__') and not isinstance(self.object, (Page, dict)):
            for item in self.object:
                list_pk.append(item.pk)
        else:
            list_pk.append(self.object.pk)

        self.list_obj_pk = list_pk


    def _rebuild_location(self):
        self.location_rebuild = {}
        locations = Locations.objects.select_related('content')\
            .filter(content__film__in=self.list_obj_pk).order_by('content__film')\
            # .values('content__film', 'content', 'type', 'lang', 'quality', 'subtitles', 'price', 'price_type', 'url_view')

        result = {}
        for item in locations:
            v = item.content.film.pk
            if not v in result:
                result[v] = []
            result[v].append(item)

        self.location_rebuild = result


    def locations_list(self, obj):
        result = self.location_rebuild.get(obj.pk, [])
        if len(result):
            return LocationsSerializer(result, many=True).data

        return result


    def poster_list(self, obj):
        result = self.poster_rebuild.get(obj.pk, [])
        if len(result):
            return [item.url for item in result if len(item.url)]

        return result


    def _rebuild_poster_list(self):
        extras = FilmExtras.objects.filter(film__in=self.list_obj_pk, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)
        extras = group_by(extras, 'id', True)

        self.poster_rebuild = extras


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
