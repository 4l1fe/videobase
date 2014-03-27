# coding: utf-8

from tastypie.api import Api
from apps.films.api import *


v1_api = Api(api_name='v1')
v1_api.register(FilmResource())


__all__ = ['v1_api']
