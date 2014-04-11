# coding: utf-8

from django.http import Http404
from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from tastypie.validation import FormValidation

from apps.films.api.serializers import vbFilm
from apps.films.forms import SearchForm



#############################################################################################################
# Api для поиска фильмов
class FilmsSearchResource(vbFilm):
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

    class Meta(vbFilm.Meta):
        allowed_methods = ['post']
        resource_name = 'films/search'
        validation = FormValidation(form_class=SearchForm)


    def prepend_urls(self):
        """
        Returns a URL scheme based on the default scheme to specify
        the response format as a file extension, e.g. /api/v1/users.json
        """
        return [
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
        ]


    def determine_format(self, request):
        """
        Used to determine the desired format from the request.format attribute.
        """
        if (hasattr(request, 'format') and
                request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(FilmsSearchResource, self).determine_format(request)


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
            'items':     bundles,
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
