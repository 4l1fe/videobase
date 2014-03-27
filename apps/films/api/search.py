# coding=utf-8

from django.contrib.auth.models import User
from tastypie.resources import ModelResource

from apps.films.models import Films


#############################################################################################################
#
class FilmResource(ModelResource):

    class Meta:
        queryset =  Films.objects.all()
        resource_name = 'films/search'
        allowed_methods = ['get']
        always_return_data = True
        fields = ['']

        # def dehydrate(self, bundle):
        #     fields = ['page', 'total_cnt', 'per_page', 'items']

