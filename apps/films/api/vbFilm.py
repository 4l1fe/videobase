# coding: utf-8

from tastypie import fields
from tastypie.resources import ModelResource, csrf_exempt

from utils.common import group_by, reindex_by, list_of

from apps.films.models import Films, FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER

from apps.contents.models import Contents, Locations



__all__ = ['vbFilm']

#############################################################################################################
# Api для поиска фильмов
class vbFilm(ModelResource):
    ratings   = fields.DictField(readonly=True)
    poster    = fields.ListField(readonly=True)
    relation  = fields.DictField(readonly=True)
    locations = fields.ListField(readonly=True)

    class Meta:
        object_class = Films
        queryset = Films.get_film_type.all()

        include_resource_uri = False
        always_return_data = True
        fields = ['id', 'name', 'name_orig', 'release_date', 'poster', \
                  'relation', 'ratings', 'duration', 'locations',\
                 ]

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(vbFilm, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper


    def get_films_extras(self, list_ids):
        extras = FilmExtras.objects.filter(film__in=list_ids, etype=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)
        return group_by(extras, 'id', True)


    def get_films_locations(self, list_ids):
        # Select contents by films
        contents = Contents.objects.filter(film__in=list_ids).values('id', 'film')
        contents = list_of(contents, 'id', True, True)

        # Select locations contents by contents
        locations = Locations.objects.filter(content__in=contents)
        locations = reindex_by(locations, 'content', True)

        # Rebuild data
        result = {}
        for item in contents:
            result[item.film] = locations[item.id]

        return result


    def dehydrate_ratings(self, bundle):
        obj = bundle.obj
        ratings = {
            'imdb': [obj.rating_imdb, obj.rating_imdb_cnt],
            'kp': [obj.rating_kinopoisk, obj.rating_kinopoisk_cnt],
            'cons': [0, 0],
        }

        return ratings


    def dehydrate_relation(self, bundle):
        relation = {}
        if bundle.request.user.is_authenticated():
            relation = {
                'subscribed': False,
                'status': '',
                'ratring': '',
            }

        return relation


    def dehydrate_poster(self, bundle):
        obj = bundle.obj
        if hasattr(obj, 'poster'):
            return [item.url for item in obj.poster if len(item.url)]

        return []


    def dehydrate_locations(self, bundle):
        obj = bundle.obj
        if hasattr(obj, 'locations'):
            return obj.locations

        return []
