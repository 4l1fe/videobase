# coding: utf-8

from django.db.models import Q
from django.core.paginator import Page

from rest_framework import serializers

from apps.films.models import *
from apps.contents.models import *
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER,\
                                 APP_PERSON_DIRECTOR, APP_PERSON_SCRIPTWRITER

from utils.common import group_by
from utils.middlewares.local_thread import get_current_request

from vb_person import vbPerson


#############################################################################################################
class CountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id', 'name')


#############################################################################################################
class GentriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'name')


#############################################################################################################
class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations


#############################################################################################################
class ContentSerializer(serializers.ModelSerializer):
    film = LocationsSerializer()

    class Meta:
        model = Locations
        fields = ('id', 'film',)


#############################################################################################################
class vbFilm(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField('poster_list')
    ratings = serializers.SerializerMethodField('calc_ratings')
    relation = serializers.SerializerMethodField('relation_list')
    releasedate = serializers.SerializerMethodField('calc_release')
    locations = serializers.SerializerMethodField('locations_list')

    # Признак extend
    countries = CountriesSerializer()
    genres = GentriesSerializer()
    directors = serializers.SerializerMethodField('director_list')
    scriptwriters = serializers.SerializerMethodField('scriptwriter_list')

    # Признак person
    persons = vbPerson()


    def __init__(self, *args, **kwargs):
        new_fields = []

        self.extend_sign = kwargs.pop('extend', False)
        if not self.extend_sign:
            new_fields += ['description', 'genres', 'countries', 'directors', 'scriptwriters']

        self.persons_sign = kwargs.pop('persons', False)
        if not self.persons_sign:
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
        self._rebuild_tors_list()


    def _rebuild_tors_list(self):
        directors_list = []
        scriptwriters_list = []

        if self.extend_sign:
            o_person = Persons.objects.filter(Q(person_film_rel__p_type=APP_PERSON_DIRECTOR) | Q(person_film_rel__p_type=APP_PERSON_SCRIPTWRITER),
                                              person_film_rel__film__in=self.list_obj_pk).\
                extra(select={'p_type': "persons_films.p_type"}).order_by('id')

            for item in o_person:
                if item.p_type == APP_PERSON_DIRECTOR:
                    directors_list.append(item)
                else:
                    scriptwriters_list.append(item)

        self.tors_list = {
            'directors': directors_list,
            'scriptwriters': scriptwriters_list,
        }


    def calc_ratings(self, obj):
        return {
            'imdb': [obj.rating_imdb, obj.rating_imdb_cnt],
            'kp': [obj.rating_kinopoisk, obj.rating_kinopoisk_cnt],
            'cons': [0, 0],
        }


    def calc_release(self, obj):
        return obj.release_date


    def _get_obj_list(self):
        list_pk = []
        instance = self.object
        if hasattr(instance, '__iter__') and not isinstance(instance, (Page, dict)):
            for item in instance:
                list_pk.append(item.pk)
        else:
            list_pk.append(instance.pk)

        self.list_obj_pk = list_pk


    def _rebuild_location(self):
        locations = Locations.objects.filter(content__film__in=self.list_obj_pk)\
            .order_by('content__film').select_related('content')
            # .values('content__film', 'content', 'type', 'lang', 'quality', 'subtitles', 'price', 'price_type', 'url_view')

        result = {}
        for item in locations:
            v = item.content.film_id
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
            return [item.url for item in result if not item.url is None and len(item.url)]

        return result


    def _rebuild_poster_list(self):
        extras = FilmExtras.objects.filter(film__in=self.list_obj_pk, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)
        extras = group_by(extras, 'id', True)

        self.poster_rebuild = extras


    def relation_list(self, obj):
        request = get_current_request()
        if request.user.is_authenticated():
            return {
                'subscribed': True,
                'status': True,
                'rating': True,
            }

        return {}


    def director_list(self, obj):
        temp = self.tors_list['directors']
        if len(temp):
            return vbPerson(temp, many=True).data

        return temp


    def scriptwriter_list(self, obj):
        temp = self.tors_list['scriptwriters']
        if len(temp):
            return vbPerson(temp, many=True).data

        return temp


    class Meta:
        model = Films
        fields = ['id', 'name', 'name_orig', 'releasedate', \
                  'ratings', 'duration', 'locations', 'poster', 'relation', \
                  'description', 'countries', 'directors', 'scriptwriters', \
                  'genres', 'persons',
                 ]
