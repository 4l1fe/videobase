# coding: utf-8

from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt

from apps.films.models import Films

#############################################################################################################
#
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

    # text     = fields.CharField(null=True, blank=True)
    # genre    = fields.CharField(null=True, blank=True)
    # year_old = fields.CharField(null=True, blank=True)
    # rating   = fields.CharField(null=True, blank=True)
    # price    = fields.CharField(null=True, blank=True)
    # page     = fields.CharField(null=True, blank=True)
    # instock  = fields.CharField(null=True, blank=True)

    class Meta:
        queryset = Films.objects.all()
        # object_class = Films
        resource_name = 'films/search'
        list_allowed_methods = ['post', 'get', 'put', 'patch']
        include_resource_uri = False
        always_return_data = True
        # excludes = ['id']
        fields = ['id', 'name']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


    # def deserialize(self, request, data, format=None):
    #     if request.POST:
    #         data = request.POST.copy()
    #         return data
    #     else:
    #         return super(FilmsSearchResource, self).deserialize(request, data, format)

    def determine_format(self, request):
        return 'application/json'

    def hydrate(self, bundle):
        request_method=bundle.request.META['REQUEST_METHOD']
        print "ok dfdsf"

        if request_method == 'POST':
            print "POST"

            #do something if you want
        elif request_method == 'PUT':
            print "PUT"
            #do something if you want

        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        resp = {}
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                resp['total_cnt'] = data_dict['meta']['total_count']
                resp['per_page'] = data_dict['meta']['limit']
                resp['page'] = (data_dict['meta']['offset'] / data_dict['meta']['limit']) + 1
                del data_dict['meta']

            resp['items'] = {}
            if 'objects' in data_dict:
                resp['items'] = data_dict['objects']

            data_dict['objects'] = resp

        return resp

    # def obj_create(self, bundle, **kwargs):
    #     bundle = self.full_hydrate(bundle)
    #     print kwargs
    #     return bundle
