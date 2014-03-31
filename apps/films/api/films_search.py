# coding: utf-8

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from apps.films.forms import SearchForm
from apps.films.models import Films


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

    class Meta:
        object_class = Films
        queryset = Films.objects.all()
        validation = FormValidation(form_class=SearchForm)

        resource_name = 'films/search.json'
        allowed_methods = ['post']

        include_resource_uri = False
        always_return_data = True
        fields = ['id', 'name', 'name_org', 'release_date', 'poster', \
                  'relation', 'ratings', 'duration', 'locations',\
                 ]


    def determine_format(self, request):
        return 'application/json'


    def alter_list_data_to_serialize(self, request, page):
        bundles = []

        for obj in page.object_list:
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

        return data, filter


    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized, filter = self.alter_deserialized_detail_data(request, deserialized)

        o_search = self._meta.queryset.filter(**filter)
        paginator = Paginator(o_search, 24)

        try:
            page = paginator.page(int(deserialized.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        object_list = self.alter_list_data_to_serialize(request, page)
        self.log_throttled_access(request)

        return self.create_response(request, object_list)
