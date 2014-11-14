# coding: utf-8

from collections import defaultdict

from django.db.models import Q
from django.core.paginator import Page

from rest_framework import serializers

from apps.films.models import *
from apps.contents.models import *
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_SCRIPTWRITER

from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_FREE
from utils.common import group_by
from utils.middlewares.local_thread import get_current_request

from vb_person import vbPerson



#############################################################################################################
class CountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ('id', 'name')


#############################################################################################################
class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'name')


#############################################################################################################
class LocationsSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('calc_price')

    def calc_price(self,obj):
        return float(obj.price)

    class Meta:
        model = Locations
        
        fields = (
            'id', 'type', 'lang', 'quality', 'subtitles',
            'price', 'price_type', 'url_view', 'value'
        )


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
    hasFree = serializers.SerializerMethodField('calc_has_free')
    instock = serializers.SerializerMethodField('calc_instock')

    # Признак extend
    countries = CountriesSerializer()
    genres = serializers.SerializerMethodField('genres_list')
    directors = serializers.SerializerMethodField('director_list')
    scriptwriters = serializers.SerializerMethodField('scriptwriter_list')

    # Признак person
    persons = serializers.SerializerMethodField('persons_list')

    def __init__(self, *args, **kwargs):
        new_fields = []

        # Get extend sign
        self.extend_sign = kwargs.pop('extend', False)
        if not self.extend_sign:
            new_fields += ['description', 'genres', 'countries', 'directors', 'scriptwriters']

        # Get person sign
        self.persons_sign = kwargs.pop('persons', False)
        if not self.persons_sign:
            new_fields += ['persons']

        request = kwargs.pop('request', False)
        require_relation = kwargs.pop('require_relation', True)

        # Instantiate the superclass normally
        super(vbFilm, self).__init__(*args, **kwargs)

        if len(new_fields):
            # Drop keys if they exist
            for field_name in new_fields:
                self.fields.pop(field_name, None)

        self._get_obj_list()
        self._rebuild_location()
        self._rebuild_poster_list()
        self._rebuild_relation_list(request, require_relation)

        if self.extend_sign:
            self._rebuild_tors_list()
            self._rebuild_genres()

    def calc_release(self, obj):
        return obj.release_date

    def persons_list(self, obj):
        o_persons = Persons.objects.filter(pf_persons_rel__film=obj).\
            exclude(Q(pf_persons_rel__p_type=APP_PERSON_DIRECTOR) | Q(pf_persons_rel__p_type=APP_PERSON_SCRIPTWRITER)).\
            extra(select={'p_type': "persons_films.p_type", 'film': "persons_films.film_id"}).\
            order_by('id')

        return vbPerson(o_persons, many=True).data

    def calc_ratings(self, obj):
        return obj.get_rating_for_vb_film

    def calc_has_free(self, obj):
        for loc in self.location_rebuild.get(obj.pk, []):
            if loc.price_type == APP_CONTENTS_PRICE_TYPE_FREE:
                return True

        return False

    def calc_instock(self, obj):
        if len(self.location_rebuild.get(obj.pk, [])):
            return True

        return False

    def _get_obj_list(self):
        list_pk = []
        instance = self.object
        if hasattr(instance, '__iter__') and not isinstance(instance, (Page, dict)):
            list_pk = [item.id for item in instance]
        else:
            list_pk.append(instance.id)

        self.list_obj_pk = list_pk

    # ---------------------------------------------------------------------------------------
    def _rebuild_genres(self):
        result = defaultdict(list)
        for item in Genres.get_full_genres_by_films(self.list_obj_pk):
            result[item.films_id].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        self.genres_rebuild = result

    def genres_list(self, obj):
        return self.genres_rebuild.get(obj.pk, [])

    # ---------------------------------------------------------------------------------------
    def _rebuild_location(self):
        locations = Locations.objects.filter(content__film__in=self.list_obj_pk)\
            .order_by('price', 'content__film', 'content__id').select_related('content')

        result = defaultdict(list)
        for item in locations:
            result[item.content.film_id].append(item)

        self.location_rebuild = result

    def locations_list(self, obj):
        result = self.location_rebuild.get(obj.pk, [])
        if len(result):
            return LocationsSerializer(result, many=True).data

        return result

    # ---------------------------------------------------------------------------------------
    def _rebuild_poster_list(self):
        extras = FilmExtras.get_additional_material_by_film(self.list_obj_pk)
        self.poster_rebuild = group_by(extras, 'film_id', True)

    def poster_list(self, obj):
        result = self.poster_rebuild.get(obj.pk, '')

        if len(result):
            url_result = ''
            for item in result:
                if not item.photo is None and item.photo:
                    url_result = item.get_photo_url()
                    break

            return url_result

        return result

    # ---------------------------------------------------------------------------------------
    def _rebuild_relation_list(self, request, require_relation):
        result = defaultdict(list)

        if require_relation:
            def check_auth(request):
                return request.user.is_authenticated()

            if request:
                is_auth = check_auth(request)
            else:
                request = get_current_request()
                is_auth = check_auth(request)

            if is_auth:
                o_user = UsersFilms.objects.filter(user=request.user, film__in=self.list_obj_pk)
                for item in o_user:
                    result[item.film_id] = item.relation_for_vb_film

        self.relation_rebuild = result

    def relation_list(self, obj):
        return self.relation_rebuild.get(obj.pk, {})

    # ---------------------------------------------------------------------------------------
    def _rebuild_tors_list(self):
        result = {}

        o_person = Persons.objects.\
            filter(Q(pf_persons_rel__p_type=APP_PERSON_DIRECTOR) | Q(pf_persons_rel__p_type=APP_PERSON_SCRIPTWRITER),
                                          pf_persons_rel__film__in=self.list_obj_pk).\
            extra(select={
                'p_type': 'persons_films.p_type',
                'film': 'persons_films.film_id'
            }).order_by('id')

        for key, value in group_by(o_person, 'film', True).items():
            if not key in result:
                result[key] = {
                    'directors': [],
                    'scriptwriters': [],
                }

            for item in value:
                if item.p_type == APP_PERSON_DIRECTOR:
                    result[key]['directors'].append(item)
                else:
                    result[key]['scriptwriters'].append(item)

        self.tors_list = result

    def director_list(self, obj):
        temp = self.tors_list.get(obj.pk, [])
        if len(temp):
            if len(temp['directors']):
                return vbPerson(temp['directors'], many=True).data
            else:
                return []

        return temp

    def scriptwriter_list(self, obj):
        temp = self.tors_list.get(obj.pk, [])
        if len(temp):
            if len(temp['scriptwriters']):
                return vbPerson(temp['scriptwriters'], many=True).data
            else:
                return []

        return temp

    class Meta:
        model = Films
        fields = [
            'id', 'name', 'name_orig', 'releasedate',
            'ratings', 'duration', 'locations', 'hasFree', 'instock',
            'poster', 'relation', 'description', 'countries',
            'directors', 'scriptwriters', 'genres', 'persons'
        ]
