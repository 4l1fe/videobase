# coding: utf-8

from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from tastypie.resources import ModelResource, csrf_exempt
from tastypie.validation import FormValidation
from tastypie import fields

from apps.films.forms import SearchForm
from apps.films.models import Films, FilmExtras
from apps.contents.models import Contents, Locations
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER
from apps.contents.models import Locations
from utils.common import group_by, reindex_by, list_of
from django.forms.models import model_to_dict

from collections import defaultdict


class LocationsResource(ModelResource):
    class Meta:
        object_class = Locations
        queryset = Locations.objects.all()
        fields = []


#############################################################################################################
# Api для поиска фильмов
class FilmsSearchResource(ModelResource):
    """
    Поиск по фильмам:
        text - Текст для поиска
        genre - id жанра
        year_old - Количество лет, прошедших с года выпуска
        rating - Рейтинг не меньше
        price - Стоимость не больше
        per_page - Количество фильмов на страницу
        page - Номер страницы
        instock - Фильм в наличии в кинотеатрах
    """

    ratings   = fields.DictField(readonly=True)
    poster    = fields.ListField(readonly=True)
    relation  = fields.DictField(readonly=True)
    locations = fields.ListField(readonly=True)

    class Meta:
        object_class = Films
        queryset = Films.get_film_type.all()
        validation = FormValidation(form_class=SearchForm)

        resource_name = 'films/search'
        allowed_methods = ['post']

        include_resource_uri = False
        always_return_data = True
        fields = ['id', 'name', 'name_orig', 'release_date', 'poster', \
                  'relation', 'ratings', 'duration', 'locations',\
                 ]


    def prepend_urls(self):
        """
        Returns a URL scheme based on the default scheme to specify
        the response format as a file extension, e.g. /api/v1/users.json
        """
        return [
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            # url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
            # url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


    def determine_format(self, request):
        """
        Used to determine the desired format from the request.format attribute.
        """
        if (hasattr(request, 'format') and
                request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(FilmsSearchResource, self).determine_format(request)


    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(FilmsSearchResource, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper


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
        return [item.url for item in bundle.obj.poster if len(item.url)]


    def dehydrate_locations(self, bundle):
        return bundle.obj.locations


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


    def alter_list_data_to_serialize(self, request, page):
        bundles = []

        list_ids = [i.pk for i in page.object_list]
        extras = self.get_films_extras(list_ids)
        locations = self.get_films_locations(list_ids)

        for obj in page.object_list:
            obj.poster = extras.get(obj.pk, [])
            obj.locations = locations.get(obj.pk, [])
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        object_list = {
            'total_cnt': page.paginator.num_pages,
            'per_page':  page.paginator.per_page,
            'page':      page.number,
            'objects':   bundles,
        }

        return object_list


    def alter_deserialized_detail_data(self, request, data):
        filter = {}
        if data.get('text'):
            filter.update({'name': data['text']})

        if data.get('genre'):
            filter.update({'genre': data['genre']})

        if data.get('rating'):
            filter.update({'rating': data['rating']})

        if data.get('price'):
            filter.update({'price': data['price']})

        if data.get('instock'):
            filter.update({'instock': data['instock']})

        return data, filter


    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized, filter = self.alter_deserialized_detail_data(request, deserialized)

        o_search = self._meta.queryset.filter(**filter)
        paginator = Paginator(o_search, deserialized.get('per_page', 24))

        try:
            page = paginator.page(int(deserialized.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        object_list = self.alter_list_data_to_serialize(request, page)
        self.log_throttled_access(request)

        return self.create_response(request, object_list)
