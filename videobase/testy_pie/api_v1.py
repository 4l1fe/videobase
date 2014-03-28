# coding: utf-8

from tastypie.api import Api
from apps.films.api import *


api_v1 = Api(api_name='v1')
api_v1.register(FilmResource())


__all__ = ['api_v1']
